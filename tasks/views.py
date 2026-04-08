import csv
import json  # Used for Chart.js data and Offline Sync
from datetime import timedelta
from django.utils import timezone
from django.db.models.functions import TruncDay
from django.http import HttpResponse, JsonResponse  # Added JsonResponse for sync
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from .models import Task, Category, Priority, SubTask, Note
from .forms import TaskForm
from django.contrib.messages.views import SuccessMessageMixin

# --- AUTHENTICATION VIEWS ---

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to Hangarin! Your account has been created.")
            return redirect('task_list')
        else:
            messages.error(request, "There was an error with your registration.")
    else:
        form = UserCreationForm()
    
    return render(request, 'account/signup.html', {'form': form})


# --- TASK MANAGEMENT VIEWS ---

@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    priority_filter = request.GET.get('priority', '')
    has_subtasks = request.GET.get('has_subtasks', '') 
    has_notes = request.GET.get('has_notes', '')      
    sort_by = request.GET.get('sort_by', '-created_at')
    
    tasks_query = Task.objects.select_related('category', 'priority').annotate(
        subtask_count=Count('subtasks'),
        note_count=Count('notes')
    ).filter(user=request.user)
    
    if category_filter:
        tasks_query = tasks_query.filter(category__name__iexact=category_filter)

    if priority_filter:
        tasks_query = tasks_query.filter(priority__name__iexact=priority_filter)

    if has_subtasks == 'true':
        tasks_query = tasks_query.filter(subtask_count__gt=0)

    if has_notes == 'true':
        tasks_query = tasks_query.filter(note_count__gt=0)

    if search_query:
        tasks_query = tasks_query.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    try:
        tasks_query = tasks_query.order_by(sort_by)
    except Exception:
        tasks_query = tasks_query.order_by('-created_at')
        sort_by = '-created_at'
    
    completed_count = tasks_query.filter(status__iexact='Completed').count()
    in_progress_count = tasks_query.filter(status__iexact='In Progress').count()
    pending_count = tasks_query.filter(status__iexact='Pending').count()
    
    all_categories = Category.objects.all() 

    return render(request, 'task_list.html', {
        'tasks': tasks_query,
        'completed_count': completed_count,
        'in_progress_count': in_progress_count,
        'pending_count': pending_count,
        'is_paginated': False, 
        'current_sort': sort_by,
        'categories': all_categories,
        'active_category': category_filter,
        'active_priority': priority_filter,
    })

@login_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            Category.objects.get_or_create(name=name)
            messages.success(request, f"Category '{name}' added!")
    return redirect('task_list')

@login_required
def export_tasks(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hangarin_tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Priority', 'Status', 'Deadline'])
    
    tasks = Task.objects.filter(user=request.user).select_related('category', 'priority')
    for t in tasks:
        cat_name = t.category.name if t.category else "None"
        prio_name = t.priority.name if t.priority else "None"
        writer.writerow([t.title, cat_name, prio_name, t.status, t.deadline])
    return response


# --- SUBTASK & NOTE QUICK-ADD VIEWS ---

@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            SubTask.objects.create(parent_task=task, title=title) 
            messages.success(request, "Subtask added!")
    return redirect('task_detail', pk=task.id)

@login_required
def add_note(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        content = request.POST.get('content')
        if content:
            Note.objects.create(task=task, content=content)
            messages.success(request, "Note added!")
    return redirect('task_detail', pk=task.id)


# --- TASK CRUD VIEWS ---

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = "Task created successfully!"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # NEW: Handle Offline Sync JSON requests within the same view
    def post(self, request, *args, **kwargs):
        if request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                
                # Retrieve related objects safely
                category_obj = None
                if data.get('category'):
                    category_obj = Category.objects.filter(name__iexact=data.get('category')).first()
                
                priority_obj = None
                if data.get('priority'):
                    priority_obj = Priority.objects.filter(name__iexact=data.get('priority')).first()

                # Save the queued task from the phone/browser
                Task.objects.create(
                    user=request.user,
                    title=data.get('title'),
                    description=data.get('description', ''),
                    category=category_obj,
                    priority=priority_obj,
                    status=data.get('status', 'Pending'),
                    deadline=data.get('deadline') if data.get('deadline') else None
                )
                return JsonResponse({'status': 'success', 'message': 'Offline task synced'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        # If standard form (Online), use default CreateView behavior
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'task'

    def get_queryset(self):
        return self.model.objects.select_related('category', 'priority').prefetch_related('subtasks', 'notes').filter(user=self.request.user)

class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = "Task updated successfully!"

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def post(self, request, *args, **kwargs):
        messages.warning(self.request, "Task deleted.")
        return super().post(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)


@login_required
def dashboard_analytics(request):
    user_tasks = Task.objects.filter(user=request.user)
    
    # 1. Stat Card Calculations
    total_tasks_count = user_tasks.count()
    
    today = timezone.now().date()
    completed_today_count = user_tasks.filter(
        status__iexact='Completed', 
        completed_at__date=today
    ).count()

    total_completed_count = user_tasks.filter(status__iexact='Completed').count()

    critical_count = user_tasks.filter(priority__name__iexact='Critical').count()

    unique_categories_count = user_tasks.exclude(category__isnull=True).values('category').distinct().count()
    
    # 2. Chart Aggregations
    category_data = user_tasks.values('category__name').annotate(count=Count('id'))
    priority_data = user_tasks.values('priority__name').annotate(count=Count('id'))
    
    last_week = timezone.now() - timedelta(days=7)
    trend_qs = (
        user_tasks.filter(status__iexact='Completed', completed_at__gte=last_week)
        .annotate(day=TruncDay('completed_at'))
        .values('day')
        .annotate(count=Count('id'))
        .order_by('day')
    )

    context = {
        'total_tasks_count': total_tasks_count,
        'completed_today_count': completed_today_count,
        'total_completed_count': total_completed_count,
        'critical_count': critical_count,
        'unique_categories_count': unique_categories_count,

        'cat_labels': json.dumps([item['category__name'] or 'Uncategorized' for item in category_data]),
        'cat_counts': json.dumps([item['count'] for item in category_data]),
        'prio_labels': json.dumps([item['priority__name'] or 'None' for item in priority_data]),
        'prio_counts': json.dumps([item['count'] for item in priority_data]),
        'trend_labels': json.dumps([item['day'].strftime('%a, %b %d') for item in trend_qs]),
        'trend_counts': json.dumps([item['count'] for item in trend_qs]),
    }
    
    return render(request, 'analytics.html', context)