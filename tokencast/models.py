from django.db import models
from django.conf import settings
import random
import uuid

class PollSession(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token_no = models.CharField(max_length=10, unique=True)
    verification_code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    head_count = models.PositiveIntegerField()
    course_name = models.CharField(max_length=255)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def generate_token(self):
        self.token_no = str(random.randint(100000, 999999))
        self.save()
       
class StudentVote(models.Model):
    poll_session = models.ForeignKey(PollSession, on_delete=models.CASCADE)
    token_no = models.CharField(max_length=10)
    vote = models.CharField(max_length=100)
    submitted_at = models.DateTimeField(auto_now_add=True)
