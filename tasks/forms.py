from django import forms
from .models import Task, Category, Priority

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        # Ensure all fields you want to save are listed here
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
            self.fields['category'].empty_label = "Select Category"
            self.fields['category'].required = True # Force selection
        
        # Sort priorities by ID
        if 'priority' in self.fields:
            self.fields['priority'].queryset = Priority.objects.all().order_by('id')
            self.fields['priority'].empty_label = "Select Priority"
            self.fields['priority'].required = True # Force selection

        # Ensure deadline is required so it's not "lost"
        if 'deadline' in self.fields:
            self.fields['deadline'].required = True

# Added LoginForm to support your login.html rendering
class LoginForm(forms.Form):
    login = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username or email',
            'class': 'form-control-dark'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': '••••••••',
            'class': 'form-control-dark'
        })
    )