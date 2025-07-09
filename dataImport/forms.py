from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import  ResearchProject
import re


class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label='Upload Excel File',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx, .xls'
        })
    )
    
class ResearchUploadForm(forms.Form):
    file = forms.FileField(
        label='Upload Excel File',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx, .xls'
        })
    )

class ResearchProjectForm(forms.ModelForm):
    class Meta:
        model = ResearchProject
        fields = [
            'teacher',
            'dept_name',
            'pi_name',
            'project_title',
            'funding_agency',
            'award_year',
            'amount',
            'duration'
        ]
        labels = {
            'teacher': "Assigned Teacher",
            'dept_name': "Department Name",
            'pi_name': "Name of the PI/Co-PI",
            'project_title': "Title of the Research Project",
            'funding_agency': "Name of the Funding Agency",
            'award_year': "Year of Award or Sanction",
            'amount': "Amount in Rs.",
            'duration': "Duration (in years)",
        }
        help_texts = {
            'award_year': "Format: YYYY-YY (e.g., 2018-19)",
        }
        widgets = {
            'project_title': forms.Textarea(attrs={'rows': 3}),
            'award_year': forms.TextInput(attrs={'placeholder': 'YYYY-YY'}),
            'amount': forms.NumberInput(attrs={'step': 0.01}),
            'duration': forms.TextInput(attrs={'placeholder': 'Year-Month'}),
        }





