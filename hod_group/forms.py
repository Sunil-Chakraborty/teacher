from django import forms
from .models import StudentAdmitted
from teachers.models import  Department


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
            "acad_year": forms.TextInput(attrs={"placeholder": "e.g., 2023-24"}),
            "sanc_seats": forms.NumberInput(attrs={"min": 0}),
            "admit_seats": forms.NumberInput(attrs={"min": 0}),
            "seats_resrv_catg": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        # Fetch filtered queryset from kwargs
        programs = kwargs.pop("programs", None)
        super().__init__(*args, **kwargs)
        if programs:
            self.fields["prog_name"].queryset = programs  # Update queryset dynamically
        else:
            self.fields["prog_name"].queryset = Department.objects.none()
