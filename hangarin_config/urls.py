from django.contrib import admin
from django.urls import path, include # Added include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from tasks import views as task_views

admin.site.site_header = "Hangarin Admin"

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Dashboard & CRUD
    path('', task_views.task_list, name='task_list'),
    path('export/', task_views.export_tasks, name='export_tasks'),
    path('task/new/', task_views.TaskCreateView.as_view(), name='task_create'),
    path('task/<int:pk>/', task_views.TaskDetailView.as_view(), name='task_detail'),
    path('task/<int:pk>/edit/', task_views.TaskUpdateView.as_view(), name='task_update'),
    path('task/<int:pk>/delete/', task_views.TaskDeleteView.as_view(), name='task_delete'),

    # --- AllAuth System (Socials & Standard Auth) ---
    # This single line handles Login, Logout, Signup, and Social Callbacks
    path('accounts/', include('allauth.urls')),
    
    # Keeping your custom signup view if you prefer it over the default allauth one
    path('signup/', task_views.signup, name='signup'),
]

# Serving static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)