from django import forms

from .models import Task, UserAccess

# User Registration Form
class UserAccessForm(forms.ModelForm):
    class Meta:
        model = UserAccess
        fields = ['access_id', 'short_name', 'full_name']

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'fpr', 'target_dt']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Task Title'}),
            'fpr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Responsible Person'}),
            'target_dt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Target Date'}),
            
        }