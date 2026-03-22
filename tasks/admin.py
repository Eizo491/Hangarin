from django.contrib import admin
from .models import Category, Priority, Task, Note, SubTask

admin.site.site_header = "Hangarin"
admin.site.site_title = "Hangarin Admin Portal"
admin.site.index_title = "Welcome to Hangarin Management"

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ('title', 'status')

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ('content',)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    class Media:
        css = {
        'all': ('tasks/css/custom_admin.css',)
    }

    list_display = ('title', 'user', 'status', 'deadline', 'priority', 'category', 'updated_at')
    list_filter = ('status', 'priority', 'category', 'user')
    search_fields = ('title', 'description', 'user__username')
    list_editable = ('status', 'priority')
    inlines = [SubTaskInline, NoteInline]
    autocomplete_fields = ['category', 'priority']
    readonly_fields = ('updated_at',)

    fieldsets = (
        ('Owner & Core Info', {
            'fields': ('user', 'title', 'description')
        }),
        ('Classification', {
            'fields': (('category', 'priority', 'status'),) 
        }),
        ('Timeline', {
            'fields': ('deadline', 'updated_at'),
        }),
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'parent_task_name', 'created_at')
    list_filter = ('status',)
    search_fields = ('title',)

    def parent_task_name(self, obj):
        return obj.parent_task.title
    parent_task_name.short_description = 'Parent Task'

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('task', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)