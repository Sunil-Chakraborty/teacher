from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone
import os
from uuid import uuid4

# Create your models here.

# Custom UserManager to handle superuser creation without 'username'

# Custom UserManager to handle superuser creation without 'username'
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

# Custom User model
class CustomUser(AbstractUser):
    username = None  # Remove the username field
    email = models.EmailField(unique=True)
    emp_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    

    USERNAME_FIELD = 'email'  # Use email as the login field
    REQUIRED_FIELDS = ['first_name', 'last_name', 'emp_id']  # Fields required when creating a user

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name}({self.email})"
               
def get_image_path(instance, filename):    
    return os.path.join('general', f"user_{instance.id}", filename)


class Teacher(models.Model):
    user = models.OneToOneField(
        "CustomUser",
        null=True,
        on_delete=models.SET_NULL,
        related_name="teachers"
    )  # Refers to the CustomUser model
    
    email = models.EmailField(unique=True)
    emp_id = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(verbose_name='Full Name', max_length=100, blank=True, null=True)  # Move first_name here
    dept_name = models.CharField(max_length=100, blank=True, null=True)  # Move first_name here
    group_name = models.CharField(max_length=100, null=True, blank=True) 
    
    dob = models.DateField(verbose_name='Date of Birth', null=True, blank=True)
    
    GENDER_CHOICES = (
        (None, 'Select Gender'),       
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        verbose_name='Gender',
        max_length=6, 
        choices=GENDER_CHOICES, 
        null=True, 
        blank=True
    )
    
    CAST_CHOICES = (
        (None, 'Select Caste'),
        ('cast-1', 'SC'),
        ('cast-2', 'ST'),
        ('cast-3', 'OBC-A'),
        ('cast-4', 'OBC-B'),
        ('cast-5', 'GEN'),
    )
    caste = models.CharField(
        verbose_name='Caste', 
        max_length=6,
        choices=CAST_CHOICES, 
        null=True, 
        blank=True
    )
    
    DESIGNATION_CHOICES = (
        (None, 'Select Designation'),
        ('dsg-1', 'Assistant Professor'),
        ('dsg-2', 'Associate Professor'),
    )
    designation = models.CharField(
        max_length=30, 
        choices=DESIGNATION_CHOICES, 
        null=True, 
        blank=True
    )
    
    doj = models.DateField(
        verbose_name='Date of Joining', 
        null=True, 
        blank=True
    )
    
    exp = models.IntegerField(
        verbose_name='Experience (in years)', 
        default=0
    )
    
    mobile = models.CharField(
        verbose_name="Mobile Number", 
        max_length=10,
        help_text="Enter a 10-digit mobile number without spaces or special characters.",       
        null=True, 
        blank=True
    )
    
    photo = models.ImageField(
        verbose_name='Photo',
        upload_to=get_image_path, 
        null=True, 
        blank=True
    )
    
    created_date = models.DateTimeField(default=timezone.now)
    
    updated_date = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"{self.user.email if self.user else 'Unknown User'}"
        

def get_quali_path(instance, filename):
    # Use the teacher's ID or other stable identifier
    teacher_id = instance.teacher.id if instance.teacher else "unknown_teacher"
    return os.path.join("general", f"user_{teacher_id}", filename)

    
class Qualification(models.Model):
    teacher      = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    
    degree       = models.CharField(
        verbose_name='Degree/Certificate',
        max_length=200, null=True, blank=True
    )
    
    subject      = models.CharField(
        verbose_name='Subject',
        max_length=200, null=True, blank=True
    )
    
    thesis       = models.CharField(
        verbose_name='Title of Dissertation/Thesis',
        max_length=400, 
        null=True, blank=True
    )
    
    institution  = models.CharField(
        verbose_name='Name of University/Institute',
        max_length=200, 
        null=True, blank=True
    )
    
    dt_award     = models.DateField(
        verbose_name='Date of Award', 
        null=True, blank=True
    )
    
    award_doc    = models.FileField(
        verbose_name="Upload Award Letters",
        upload_to=get_quali_path, null=True, 
        blank=True
    )
    
    created_date = models.DateTimeField(default=timezone.now)
    
    updated_date = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        # Save instance first to ensure `id` is assigned
        if not self.id:
            super().save(*args, **kwargs)

        # Update the upload_to path dynamically
        self.award_doc.field.upload_to = get_quali_path
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.degree} from {self.institution}"
        

class Publication(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    journal = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    def __str__(self):
        return self.title
        
class Department(models.Model):
    name    =   models.CharField(max_length=100,  null=True, blank=True)
    faculty =   models.CharField(max_length=100,  null=True, blank=True)
    program =   models.CharField(max_length=200,  null=True, blank=True)
 
    def __str__(self):
        #return f"{self.name} - {self.program}"  # Include program in the string representation
        return f"{self.name}"  # Include program in the string representation
        