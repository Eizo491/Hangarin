import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Task
from .forms import TaskForm

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

@login_required
def task_list(request):
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    tasks_query = Task.objects.select_related('category', 'priority').filter(user=request.user).order_by('-created_at')
    
    if category_filter:
        tasks_query = tasks_query.filter(category__name__iexact=category_filter)

    if search_query:
        tasks_query = tasks_query.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(tasks_query, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'task_list.html', {
        'tasks': page_obj, 
        'page_obj': page_obj, 
        'is_paginated': page_obj.has_other_pages()
    })

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

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_detail.html'
    
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task_list')
    
    def form_valid(self, form):
        messages.success(self.request, "Task updated!")
        return super().form_valid(form)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Task deleted.")
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)