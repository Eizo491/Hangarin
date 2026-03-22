from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control rounded-3', 'placeholder': 'Task Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control rounded-3', 'rows': 3, 'placeholder': 'Details...'}),
            'category': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'priority': forms.Select(attrs={'class': 'form-select rounded-3'}),
            'status': forms.Select(attrs={'class': 'form-select rounded-3'}),
        }