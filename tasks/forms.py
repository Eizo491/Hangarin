from django import forms
from .models import Task, Category, Priority

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'category', 'priority', 'status', 'deadline']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control px-4 py-2', 
                'placeholder': 'What needs to be done?'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control px-4 py-3 rounded-4', 
                'rows': 3, 
                'placeholder': 'Add some specific details here...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select px-4'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select px-4'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select px-4'
            }),
            'deadline': forms.DateInput(attrs={
                'class': 'form-control px-4', 
                'type': 'date'
            }),
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        
        # Sort Categories alphabetically
        if 'category' in self.fields:
            self.fields['category'].queryset = Category.objects.all().order_by('name')
        
        # FIX: Changed 'level' to 'id' to resolve the FieldError
        # This sorts priorities by the order they were created in the database
        if 'priority' in self.fields:
            self.fields['priority'].queryset = Priority.objects.all().order_by('id')

        # Ensures the empty labels look clean in the dropdowns
        self.fields['category'].empty_label = "Select Category"
        self.fields['priority'].empty_label = "Select Priority"