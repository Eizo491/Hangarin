from django.apps import AppConfig

class TasksConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks'

    def ready(self):
        from django.contrib import admin
        admin.site.site_header = "Hangarin Admin"
        admin.site.site_title = "Hangarin Task Manager"
        admin.site.index_title = "Welcome to Hangarin Portal"