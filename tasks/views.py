import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count # Added Count for filtering
from .models import Task, Category, Priority, SubTask, Note # Added SubTask and Note models
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
    has_subtasks = request.GET.get('has_subtasks', '') # New filter
    has_notes = request.GET.get('has_notes', '')       # New filter
    sort_by = request.GET.get('sort_by', '-created_at')
    
    # PERFORMANCE: Use select_related for FKs and annotate for filtering on counts
    tasks_query = Task.objects.select_related('category', 'priority').annotate(
        subtask_count=Count('subtasks'),
        note_count=Count('notes')
    ).filter(user=request.user)
    
    # --- FILTERING LOGIC ---
    
    if category_filter:
        tasks_query = tasks_query.filter(category__name__iexact=category_filter)

    if priority_filter:
        tasks_query = tasks_query.filter(priority__name__iexact=priority_filter)

    # Filter tasks that have at least one subtask
    if has_subtasks == 'true':
        tasks_query = tasks_query.filter(subtask_count__gt=0)

    # Filter tasks that have at least one note
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
    
    # --- STATS LOGIC ---
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


# --- NEW: SUBTASK & NOTE QUICK-ADD VIEWS ---

@login_required
def add_subtask(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)
    if request.method == "POST":
        title = request.POST.get('title')
        if title:
            SubTask.objects.create(task=task, title=title) # Note: ensure field is 'task' or 'parent_task' in models.py
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
        # Optimized to pull related lists and foreign keys in one go
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