from django.db import models
from teachers.models import Department, Teacher
from django.conf import settings
import random
import uuid

class PollSession(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=50, unique=True)
    token_no = models.CharField(max_length=10)    
    course_name = models.CharField(max_length=250)
    head_count = models.IntegerField()
    is_active = models.BooleanField(default=True)
    is_started = models.BooleanField(default=False)  # ✅ New field to track poll start
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    used_token_count = models.IntegerField(default=0)  # Add default=0 to prevent NULL errors
    counter_token = models.IntegerField(default=0)  # Add default=0 to prevent NULL errors
    
    def generate_token(self):
        self.token_no = uuid.uuid4().hex[:6].upper()
    
        
class StudentVote(models.Model):
    poll_session = models.ForeignKey(PollSession, on_delete=models.CASCADE)
    token_no = models.CharField(max_length=10)    
    clarity = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating 1-5
    engagement = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating 1-5
    teaching_methods = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  # Rating 1-5
    improvement_suggestions = models.TextField(blank=True, null=True)
    additional_comments = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vote by {self.token_no} for Session {self.poll_session.id}"