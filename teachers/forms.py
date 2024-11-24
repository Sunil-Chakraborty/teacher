from django import forms
from django.contrib.auth.models import User
from .models import CustomUser, Department, Teacher, Qualification, Publication
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import DateInput

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
            'first_name': 'Full Name',  # Change label for first_name field
        }
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            'doj': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
           
            'mobile': forms.NumberInput(attrs={  # Use forms.NumberInput directly
                'class': 'form-control',
                'required': 'required',                
                'min': 2000000000,  # Minimum value for the mobile number
                'max': 9999999999,  # Maximum value for the mobile number
                'step': 1,  # Step value (for numeric input)
                'oninvalid': "this.setCustomValidity('Give proper mobile number')",  # Custom message
                'oninput': "this.setCustomValidity('')",  # Clear message on valid input
            }),
            
            'exp': forms.NumberInput(attrs={  # Use forms.NumberInput directly
                'class': 'form-control',
                'required': 'required',                
                'min': 0,  # Minimum value for the exp number
                'max': 60,  # Maximum value for the exp number
                'step': 1,  # Step value (for numeric input)
            }),
        }
       
    def __init__(self, *args, **kwargs):
        # Get the user from kwargs
        user = kwargs.pop('user', None)
        super(TeacherForm, self).__init__(*args, **kwargs)

        # Make certain fields required
        self.fields['dob'].required = True
        self.fields['exp'].required = True
        self.fields['doj'].required = True
        self.fields['designation'].required = True
        self.fields['caste'].required = True
        self.fields['gender'].required = True
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
            'dt_award': forms.DateInput(attrs={'type': 'date', 'class': 'datepicker'}),
            
        }

class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'journal', 'publication_year']
