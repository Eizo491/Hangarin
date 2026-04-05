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
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Task, Category  # Added Category model here
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


# --- TASK MANAGEMENT VIEWS (FUNCTION-BASED) ---

@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    priority_filter = request.GET.get('priority', '') # Added priority filter
    sort_by = request.GET.get('sort_by', '-created_at')
    
    # Base query: user's tasks
    tasks_query = Task.objects.select_related('category').filter(user=request.user)
    
    # 1. Apply Category Filter
    if category_filter:
        tasks_query = tasks_query.filter(category__name__iexact=category_filter)

    # 2. Apply Priority Filter (New)
    if priority_filter:
        tasks_query = tasks_query.filter(priority=priority_filter)

    # 3. Apply Search Filter
    if search_query:
        tasks_query = tasks_query.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    # 4. Apply Dynamic Ordering
    try:
        tasks_query = tasks_query.order_by(sort_by)
    except Exception:
        tasks_query = tasks_query.order_by('-created_at')
        sort_by = '-created_at'
    
    # 5. Pagination
    paginator = Paginator(tasks_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # 6. Fetch all categories for the sidebar
    # (Assuming Category model has a 'user' field, if not, remove the filter)
    all_categories = Category.objects.all() 

    return render(request, 'task_list.html', {
        'tasks': page_obj, 
        'page_obj': page_obj, 
        'is_paginated': page_obj.has_other_pages(),
        'current_sort': sort_by,
        'categories': all_categories, # Passed to base.html sidebar
    })

# --- CATEGORY CREATE VIEW (New) ---

@login_required
def category_create(request):
    if request.method == "POST":
        name = request.POST.get('name')
        if name:
            # Create the category. 
            # If your Category model has a 'user' field, use: 
            # Category.objects.get_or_create(name=name, user=request.user)
            Category.objects.get_or_create(name=name)
            messages.success(request, f"Category '{name}' added!")
        return redirect('task_list')
    return redirect('task_list')

@login_required
def export_tasks(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hangarin_tasks.csv"'
    writer = csv.writer(response)
    writer.writerow(['Title', 'Category', 'Priority', 'Status', 'Deadline'])
    
    tasks = Task.objects.filter(user=request.user)
    for t in tasks:
        writer.writerow([t.title, t.category, t.priority, t.status, t.deadline])
    return response


# --- TASK CRUD VIEWS (CLASS-BASED) ---

class TaskCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    success_message = "Task created successfully!"
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    # Add categories to context so they can be selected in the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

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