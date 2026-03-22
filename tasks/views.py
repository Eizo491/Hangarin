import csv
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
from django.views.generic import DetailView
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib import messages

@login_required
def task_list(request):
    status_filter = request.GET.get('status')
    category_filter = request.GET.get('category')
    search_query = request.GET.get('search') # New search check
    
    tasks = Task.objects.select_related('category', 'priority').all().order_by('-created_at')
    
    if status_filter:
        tasks = tasks.filter(status=status_filter)
    
    if category_filter:
        tasks = tasks.filter(category__name__iexact=category_filter)

    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

@login_required
def export_tasks(request):
    status_filter = request.GET.get('status')
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="hangarin_tasks_export.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Task Title', 'Category', 'Priority', 'Status', 'Created At'])
    
    tasks = Task.objects.all()
    if status_filter:
        tasks = tasks.filter(status=status_filter)
        
    for task in tasks:
        writer.writerow([task.title, task.category, task.priority, task.status, task.created_at])
        
    return response

class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'
    
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html' # Reuses your existing form template
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, "Task updated successfully!")
        return super().form_valid(form)

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')
    
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Task deleted.")
        return super().delete(request, *args, **kwargs)