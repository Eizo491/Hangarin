from django.db import models

class BaseModel(models.Model):
    """
    Abstract base class to provide timestamp fields for all models.
    Requirement: All models must inherit from this.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories" # Requirement

    def __str__(self):
        return self.name

class Priority(BaseModel):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities" # Requirement

    def __str__(self):
        return self.name

class Task(BaseModel):
    # Requirement: status choices (enumeration)
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
    ]

    title = models.CharField(max_length=200) 
    description = models.TextField() 
    deadline = models.DateTimeField() 
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default="Pending" # Requirement
    )
    
    # Requirement: Foreign keys to Category and Priority
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    priority = models.ForeignKey(Priority, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Note(BaseModel):
    # Requirement: relationship to Task
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='notes') 
    content = models.TextField() 

    def __str__(self):
        return f"Note for {self.task.title}"

class SubTask(BaseModel):
    # Requirement: parent_task relationship
    parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    title = models.CharField(max_length=200) 
    
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