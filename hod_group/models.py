from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone
from django.core.validators import RegexValidator
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
    acad_year = models.CharField(
        max_length=9,
        validators=[RegexValidator(r'^\d{4}(/\d{4})?$', "Enter a valid academic year (e.g., '2023' or '2023/2024').")],
        verbose_name="Academic Year",
        null=True,
        blank=True
    )
    sanc_seats = models.IntegerField(
        default=0, verbose_name="Number of Sanctioned Seats"
    )
    admit_seats = models.IntegerField(
        default=0, verbose_name="Number of Admitted Students"
    )
    CAST_CATG = (
        ('', 'Select Category'),
        ('cast-1', 'SC'),
        ('cast-2', 'ST'),
        ('cast-3', 'OBC-A'),
        ('cast-4', 'OBC-B'),
        ('cast-5', 'GEN'),
    )
    reserv_catg = models.CharField(
        max_length=7, choices=CAST_CATG, null=True, blank=True,
        verbose_name="Reserved Category Students"
    )
    seats_resrv_catg = models.IntegerField(
        default=0, verbose_name="Number of Reserved Category Students"
    )

    def __str__(self):
        return f"{self.dept_name} - {self.prog_name} ({self.teacher})"
        
        