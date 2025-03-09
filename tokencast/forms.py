from django import forms
from .models import PollSession, StudentVote

class PollSessionForm(forms.ModelForm):
    class Meta:
        model = PollSession
        fields = ['head_count','course_name']

class StudentVoteForm(forms.ModelForm):
    class Meta:
        model = StudentVote
        fields = ['token_no', 'vote']
