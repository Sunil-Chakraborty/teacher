from django import forms
from .models import PollSession, StudentVote

class PollSessionForm(forms.ModelForm):
    class Meta:
        model = PollSession
        fields = ['head_count','course_name']

class StudentVoteForm(forms.ModelForm):
    class Meta:
        model = StudentVote
        fields = ['token_no','clarity', 'engagement', 'teaching_methods', 'improvement_suggestions', 'additional_comments']
        widgets = {
            'clarity': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'engagement': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'teaching_methods': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-select'}),
            'improvement_suggestions': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'additional_comments': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }