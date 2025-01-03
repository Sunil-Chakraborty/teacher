from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone
from teachers.models import Teacher, Department


import os
from uuid import uuid4


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
    def __str__(self):
        return f"{self.dept_name} - {self.prog_name} ({self.teacher})"
        
        