from django import forms
from django.contrib.auth.models import User
from .models import (CustomUser, Department, Teacher, 
             Qualification, Patents)
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import DateInput
from datetime import date, timedelta


class UserRegistrationForm(forms.ModelForm):
    department = forms.CharField(max_length=100, required=True)  # Expect name, not ID
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ["first_name", "email", "password", "emp_id", "department"]
        
        
    
    first_name = forms.CharField(
        label="Full Name",  # Override the label
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        required=True
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def clean_emp_id(self):
        emp_id = self.cleaned_data.get("emp_id")

        # Validate emp_id: must be a 3-digit integer
        if not emp_id or not str(emp_id).isdigit() or len(str(emp_id)) != 3:
            raise forms.ValidationError("Select a valid 3-digit number.")

        return emp_id
        
        
    def clean_department(self):
        department_name = self.cleaned_data["department"]
        try:
            # Fetch the first matching Department instance
            department = Department.objects.filter(name=department_name).first()
            if not department:
                raise forms.ValidationError("Select a valid department.")
        except Department.DoesNotExist:
            raise forms.ValidationError("Select a valid department.")
        return department  # Return the Department instance
        
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
        
    def __init__(self, *args, **kwargs):
            super(UserRegistrationForm,self).__init__(*args, **kwargs)
            self.fields['emp_id'].widget.attrs['placeholder'] = '3 digits Id'
            self.fields['emp_id'].required = True
            
            
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = [
            'first_name', 'dob', 'gender', 'caste',
            'designation', 'doj', 'exp', 'mobile', 'photo'
        ]
        labels = {
            'first_name': 'Full Name',  # Custom label
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'doj': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'mobile': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'min': 2000000000,
                'max': 9999999999,
                'oninvalid': "this.setCustomValidity('Enter a valid mobile number')",
                'oninput': "this.setCustomValidity('')",
            }),
            'exp': forms.NumberInput(attrs={
                'class': 'form-control',
                'required': 'required',
                'min': 0,
                'max': 60,
            }),
        }
   
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Optional: pass user if needed
        super(TeacherForm, self).__init__(*args, **kwargs)

        # Set field requirements
        for field_name in ['dob', 'doj', 'exp', 'designation', 'caste', 'gender']:
            self.fields[field_name].required = True
        
        # Check if dob is None before performing the operation
        if self.instance.dob is not None:
            min_doj = self.instance.dob + timedelta(days=15 * 365)  # Approximation
        else:
            # Handle the case where dob is None
            min_doj = None  # Or set a default date if necessary
            
        self.fields['dob'].widget.attrs.update({'max': date.today()})
        self.fields['doj'].widget.attrs.update({'max': date.today()})
        self.fields['doj'].widget.attrs.update(
            #{'min': self.instance.dob}
            {'min': min_doj}
        )
            
        # Set first_name as readonly
        self.fields['first_name'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        #print("Cleaned Data:", cleaned_data)  # Debugging
        return cleaned_data
    
    

    
class QualificationForm(forms.ModelForm):
    class Meta:
        model = Qualification
        fields = ['degree', 'subject', 'thesis', 'institution', 
        'dt_award', 'award_doc']
        
        widgets = {
            'thesis': forms.Textarea(attrs={
                'rows': 3,  # Adjust the number of rows
                'cols': 60, # Adjust the number of columns
                'placeholder': 'Enter the title of your dissertation or thesis here...'
            }),
            
            'dt_award': forms.DateInput(attrs={
                'type': 'date', 
                'class': 'datepicker'
            }),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Optional: pass user if needed
        super(QualificationForm, self).__init__(*args, **kwargs)
        # Set field requirements
        for field_name in ['degree', 'subject', 'institution']:
            self.fields[field_name].required = True
        


class PatentForm(forms.ModelForm):
    class Meta:
        model = Patents
        #fields = '__all__'
        fields = ['dept_name','status', 'title', 'ref_no', 'dt_award', 'awarding_agency', 'patent_ecopy']
        widgets = {
            'dt_award': forms.DateInput(attrs={'type': 'date'}),
        } 
        
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Optional: pass user if needed
        super(PatentForm, self).__init__(*args, **kwargs)
        # Set field requirements
        for field_name in ['status', 'title', 'ref_no', 'dt_award', 'awarding_agency']:
            self.fields[field_name].required = True
            
        #for field in self.fields.values():
        #    field.widget.attrs['style'] = 'font-weight: bold;'    
