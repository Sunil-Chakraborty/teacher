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
            "reserv_catg",
            "seats_resrv_catg",
        ]
        widgets = {
            "acad_year": forms.TextInput(attrs={"placeholder": "e.g., 2023/2024"}),
            "sanc_seats": forms.NumberInput(attrs={"min": 0}),
            "admit_seats": forms.NumberInput(attrs={"min": 0}),
            "seats_resrv_catg": forms.NumberInput(attrs={"min": 0}),
        }

    def __init__(self, *args, **kwargs):
        programs = kwargs.pop('programs', None)  # Fetch filtered queryset from kwargs
        super().__init__(*args, **kwargs)
        if programs:
            self.fields['prog_name'].queryset = programs  # Set queryset dynamically

    def clean(self):
        """
        Add custom validation if needed (e.g., admit_seats cannot exceed sanc_seats).
        """
        cleaned_data = super().clean()
        sanc_seats = cleaned_data.get("sanc_seats")
        admit_seats = cleaned_data.get("admit_seats")

        if sanc_seats and admit_seats and admit_seats > sanc_seats:
            self.add_error("admit_seats", "Admitted students cannot exceed sanctioned seats.")

        return cleaned_data
