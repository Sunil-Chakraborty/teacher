from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone
from teachers.models import Teacher, Department
from django.urls import reverse


import os
import uuid

# Create your models here.

class StudentAdmitted(models.Model):
    teacher = models.ForeignKey(
        "teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Assigned Teacher"
    )
    dept_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Department Name"
    )
    prog_name = models.ForeignKey(
        "teachers.Department", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Programme Name"
    )
    prog_cd = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name="Programme Code"
    )
    course_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Programme/Courses Name"
    )     
    acad_year = models.CharField(
        max_length=7,
        verbose_name="Academic Year",        
        help_text="The range must be in  1990-91 to 2024-25.",
    )
    sanc_seats = models.IntegerField(
         verbose_name="Number of Sanctioned Seats"
    )
    admit_seats = models.IntegerField(
         verbose_name="Number of Admitted Students"
    )
    
   
    seats_resrv_catg = models.IntegerField(
         verbose_name="Number of Reserved Category Students"
    )
    group_id    = models.CharField(
        max_length=10,        
        verbose_name="Group Table index",
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(default=timezone.now)
    
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.dept_name} - {self.prog_name} ({self.teacher})"
        
 


class OnlineCourse(models.Model):
    teacher = models.ForeignKey(
        "teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Assigned Teacher"
    )
    dept_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Department Name"
    )
    course_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Programme/Courses Name"
    ) 
    prog_cd = models.CharField(
        max_length=20, null=True, blank=True,
        verbose_name="Programme Code"
    )    
    
    enrol_year = models.CharField(
        max_length=4,
        verbose_name="Enrollment Year",        
        help_text="The range must be in  1990 onwards",
    )
    
    contact_hrs = models.CharField(
        max_length=4,
        verbose_name="Contact hours of the course",
        help_text="Reasonable range (e.g., 1 to 100)",
    )
    
    enrol_students = models.IntegerField(
         verbose_name="Number of Students Enrolled"
    )
    
    complete_count = models.IntegerField(
         verbose_name="Number of Students completing the course"
    )

    group_id    = models.CharField(
        max_length=10,        
        verbose_name="Group Table index",
        null=True,
        blank=True
    )
    #Document Upload (Supports PDF, Word, Images)
    document = models.FileField(
        upload_to='documents/',  # Folder inside MEDIA_ROOT
        verbose_name="Upload Course Document",
        null=True,
        blank=True
    )
    created_date = models.DateTimeField(default=timezone.now)
    
    updated_date = models.DateTimeField(auto_now=True)
   
    def __str__(self):
        return f"{self.dept_name} ({self.teacher})"
        
         