from django.db import models
from django.conf import settings
from django.utils.timezone import make_aware
import pytz

from datetime import datetime
from pytz import timezone, UTC
from datetime import datetime

# IST timezone
ist = timezone('Asia/Kolkata')


def generate_access_id():
    """Generate a random 6-character access ID"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

class Teacher(models.Model):
    name            = models.CharField(max_length=100)
    department      = models.CharField(max_length=100)
    email           = models.EmailField(unique=True)
    password        = models.CharField(max_length=255)  # Store hashed passwords

    def __str__(self):
        return self.name


class VotingSession(models.Model):
    faculty = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_no = models.CharField(max_length=10, unique=True)
    course_name = models.CharField(max_length=255)
    session_start = models.DateTimeField()
    session_end = models.DateTimeField()
    student_no = models.IntegerField()

    def convert_to_ist(self):
        # Convert session_start and session_end from UTC to IST
        if self.session_start:
            self.session_start = self.session_start.astimezone(ist)
        if self.session_end:
            self.session_end = self.session_end.astimezone(ist)
        

        
class AccessID(models.Model):
    token = models.ForeignKey(VotingSession, on_delete=models.CASCADE)  # ForeignKey to VotingSession
    access_id = models.CharField(max_length=6, unique=True)  # Random access code
    used = models.BooleanField(default=False)  # ✅ Add this field


class Feedback(models.Model):
    token = models.ForeignKey('VotingSession', on_delete=models.CASCADE)
    access_id = models.ForeignKey('AccessID', on_delete=models.CASCADE)
    feedback = models.TextField()

    def __str__(self):
        return f"Feedback for {self.token} by {self.access_id}"
