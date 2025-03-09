from django.contrib import admin
from .models import Teacher, VotingSession, AccessID, Feedback

admin.site.register(Teacher)
admin.site.register(VotingSession)
admin.site.register(AccessID)
admin.site.register(Feedback)
