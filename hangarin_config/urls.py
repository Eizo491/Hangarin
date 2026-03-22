from django.contrib import admin
from django.urls import path
from tasks import views
from django.contrib.auth import views as auth_views

admin.site.site_header = "Hangarin Admin"
admin.site.site_title = "Hangarin Task Manager"
admin.site.index_title = "Welcome to Hangarin Portal"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('', views.task_list, name='task_list'),
    path('export/', views.export_tasks, name='export_tasks'),
    path('task/new/', views.TaskCreateView.as_view(), name='task_create'),
    path('login/', auth_views.LoginView.as_view(template_name='tasks/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/edit/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
]
