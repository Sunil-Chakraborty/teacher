from django import forms
from .models import StudentAdmitted, OnlineCourse
from teachers.models import  Department
from django.core.exceptions import ValidationError

class StudentAdmittedForm(forms.ModelForm):
    prog_name = forms.ModelChoiceField(
        queryset=Department.objects.none(),
        label="Program",
        empty_label="Select a Program",
    )

    class Meta:
        model = StudentAdmitted
        fields = [
            "prog_name",
            "acad_year",
            "sanc_seats",
            "admit_seats",
            "seats_resrv_catg",
        ]
        
        widgets = {
            "acad_year": forms.TextInput(
                attrs={
                    "required": "required",
                    "placeholder": "e.g., 2023-24",  # Add a placeholder
                }
            ),
            "sanc_seats": forms.NumberInput(attrs={"min": 0, "required": "required"}),
            "admit_seats": forms.NumberInput(attrs={"min": 0, "required": "required"}),
            "seats_resrv_catg": forms.NumberInput(attrs={"min": 0, "required": "required"}),
        }

    def __init__(self, *args, programs=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set queryset for prog_name dynamically
        if programs:
            self.fields["prog_name"].queryset = programs
        else:
            self.fields["prog_name"].queryset = Department.objects.none()

class OnlineCourseForm(forms.ModelForm):
    class Meta:
        model = OnlineCourse
        exclude = ['teacher', 'group_id', 'dept_name', 'created_date', 'updated_date']
        widgets = {
            'enrol_year': forms.NumberInput(attrs={                
                'class': 'form-control',
                'placeholder': 'YYYY',
                'min': '1990',    
            }),
            'contact_hrs': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Hours',
                'min': '1',
                'max': '100'
            }),
            'enrol_students': forms.NumberInput(attrs={'min': 0}),
            'complete_count': forms.NumberInput(attrs={'min': 0}),
        }
        labels = {            
            'course_name': "Course Name",
            'prog_cd': "Program Code",
            'enrol_year': "Year of Enrollment",
            'contact_hrs': "Course Contact Hours",
            'enrol_students': "Students Enrolled",
            'complete_count': "Students Completed",
        }

    