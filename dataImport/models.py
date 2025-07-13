from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone
from teachers.models import Teacher, Department
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

import os
import uuid


class ResearchProject(models.Model):
    teacher = models.ForeignKey(
        "teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Assigned Teacher"
    )
    dept_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Department Name"
    )
    pi_name = models.CharField(
        max_length=100,
        verbose_name="Name of the PI/Co-PI"
    )
    project_title = models.TextField(
        verbose_name="Title of the Research Project"
    )
    funding_agency = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Name of the Funding Agency"
    )
    award_year = models.CharField(
        max_length=9,
        verbose_name="Year of Award or Sanction",
        help_text="Format: YYYY-YY (e.g., 2018-19)"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Amount in Rs."
    )
    duration = models.CharField(
        max_length=100,
        verbose_name="Duration (in years)"
    )
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.pi_name} - {self.project_title[:40]}..."

