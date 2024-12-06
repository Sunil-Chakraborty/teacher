from django import forms
from .models import StudentAdmitted
from teachers.models import  Department
from django.core.validators import RegexValidator

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
            "acad_year": forms.TextInput(attrs={"required": "required"}),
            "sanc_seats": forms.NumberInput(attrs={"min": 0, "required": "required"}),
            "admit_seats": forms.NumberInput(attrs={"min": 0, "required": "required"}),
            "seats_resrv_catg": forms.NumberInput(attrs={"min": 0, "required": "required"}),
        }
        
    
    def __init__(self, *args, programs=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set all fields as required
        self.fields["prog_name"].required = True
        self.fields["acad_year"].required = True
        self.fields["sanc_seats"].required = True
        self.fields["admit_seats"].required = True
        self.fields["seats_resrv_catg"].required = True


        # Set queryset for prog_name dynamically
        if programs:
            self.fields["prog_name"].queryset = programs
        else:
            self.fields["prog_name"].queryset = Department.objects.none()        