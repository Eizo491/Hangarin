from django.contrib import admin
from .models import Category, Priority, Task, Note, SubTask

# Requirement: Category and Priority Admin - Display name and make searchable [cite: 55-57]
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Requirement: Task Admin - Display title, status, deadline, priority, category [cite: 46-47]
# Filters: status, priority, category [cite: 48]
# Search: title, description [cite: 49]
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'deadline', 'priority', 'category')
    list_filter = ('status', 'priority', 'category')
    search_fields = ('title', 'description')

# Requirement: SubTask Admin - Display title, status, parent_task_name [cite: 50-52]
# Filter: status[cite: 53]. Search: title [cite: 54]
@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'parent_task')
    list_filter = ('status',)
    search_fields = ('title',)

# Requirement: Note Admin - Display task, content, created_at [cite: 58-59]
# Filter: created_at[cite: 60]. Search: content [cite: 61]
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)