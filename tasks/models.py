from django.db import models
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories" # Requirement [cite: 92]

    def __str__(self):
        return self.name

class Priority(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities" # Requirement [cite: 86]

    def __str__(self):
        return self.name

class Task(BaseModel):
    # Requirement: status choices (enumeration) [cite: 67, 71]
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200) # [cite: 18]
    description = models.TextField() # [cite: 21]
    deadline = models.DateTimeField() # [cite: 23]
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="Pending" # Requirement [cite: 69, 77]
    )
    
    # Requirement: Foreign keys to Category and Priority 
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    # Add this below your Task model

class Note(BaseModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes') # [cite: 16]
    content = models.TextField() # [cite: 20]

    def __str__(self):
        return f"Note for {self.task.title}"

class SubTask(BaseModel):
    # Requirement: parent_task relationship [cite: 32]
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200) # [cite: 36]
    
    # Requirement: status choices for subtasks 
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