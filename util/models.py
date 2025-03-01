import uuid
from django.db import models
from django.urls import reverse
     
# User Access Model
class UserAccess(models.Model):
    SHORT_NAME_CHOICES = [
        ("ADMIN", "Admin"),
        ("MANAGER", "Manager"),
        ("SUPERVISOR", "Supervisor"),
        ("OPERATOR", "Operator"),
        ("INSPECTOR", "Inspector"),
    ]

    FULL_NAME_CHOICES = [
        ("System Administrator", "System Administrator"),
        ("Production Manager", "Production Manager"),
        ("Quality Supervisor", "Quality Supervisor"),
        ("Machine Operator", "Machine Operator"),
        ("Quality Inspector", "Quality Inspector"),
    ]

    access_id  = models.CharField(max_length=10, unique=True)
    short_name = models.CharField(max_length=50, choices=SHORT_NAME_CHOICES)
    full_name  = models.CharField(max_length=100, choices=FULL_NAME_CHOICES)

    def __str__(self):
        return f"{self.short_name} ({self.access_id})"
        
        
# Updated Task Model with ForeignKey
class Task(models.Model):
    user       = models.ForeignKey(UserAccess, on_delete=models.CASCADE)  # Links task to a user
    title      = models.CharField(max_length=255)
    fpr        = models.CharField(max_length=255, verbose_name="First Person Responsible")
    target_dt  = models.CharField(max_length=50, verbose_name="Target Date")
    completed  = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    # Random verification code
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def get_secure_edit_url(self):
        return reverse("util:edit_task", kwargs={"task_id": self.id, "verification_code": self.verification_code})
    
    def __str__(self):
        return self.title
    