from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Priority(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.name

class Task(BaseModel):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200) 
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField(null=True, blank=True) 
    
    # NEW FIELD: Specifically for analytics to track completion trends
    completed_at = models.DateTimeField(null=True, blank=True) 

    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="Pending"
    )
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='tasks')
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True, related_name='tasks')

    @property
    def is_completed(self):
        return self.status == "Completed"

    def save(self, *args, **kwargs):
        """
        Custom save method to automatically handle the completed_at timestamp.
        1. If status is 'Completed' and date is missing, set it to now.
        2. If status is moved away from 'Completed', clear the date.
        """
        if self.status == "Completed":
            # Only set timestamp if it wasn't already set (prevents overwriting on every edit)
            if not self.completed_at:
                self.completed_at = timezone.now()
        else:
            # If a task is moved back to 'In Progress' or 'Pending', clear the completion date
            self.completed_at = None
            
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes') 
    content = models.TextField() 

    def __str__(self):
        return f"Note for {self.task.title}"

class SubTask(BaseModel):
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200) 
    
    status = models.CharField(
        max_length=50,
        choices=Task.STATUS_CHOICES,
        default="Pending"
    )

    class Meta:
        verbose_name = "Sub Task"
        verbose_name_plural = "Sub Tasks"

    def __str__(self):
        return self.title