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
            'pi_name', 'project_title', 'funding_agency',
            'award_year', 'amount', 'duration'
        ]
        widgets = {
            'project_title': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),
            'pi_name': forms.TextInput(attrs={'class': 'form-control'}),
            'funding_agency': forms.TextInput(attrs={'class': 'form-control'}),
            'award_year': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'duration': forms.TextInput(attrs={'class': 'form-control'}),
        }

ResearchProjectFormSet = modelformset_factory(
    ResearchProject,
    form=ResearchProjectForm,
    extra=5,  # allow 5 blank forms
    can_delete=False
)
