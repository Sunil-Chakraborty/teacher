from django.db import models
from django.core.validators import RegexValidator
from teachers.models import Department


class AcademicAudit(models.Model):
    FACULTY_CHOICES = [
        ('ARTS', 'ARTS'),
        ('Sc', 'Science'),
        ('Engg', 'Engineering'),
        ('ISLM', 'ISLM'),
    ]

    faculty = models.CharField(max_length=10, choices=FACULTY_CHOICES)
    dept_school = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='academic_audits'
    )
    name_hod = models.CharField(max_length=200)
    contact_number_office = models.CharField(max_length=20, blank=True)
    contact_number_hod = models.CharField(max_length=20, blank=True)
    vision = models.TextField()
    mission = models.TextField()
    academic_year = models.CharField(
        max_length=9,
        validators=[
            RegexValidator(
                regex=r'^\d{4}[-–]\d{2}$',  # matches hyphen (-) or en dash (–)
                message="Academic year must be in format YYYY–YY or YYYY-YY (e.g., 2024–25)"
            )
        ]
    )
    spl_assistant_prog = models.BooleanField(default=False)

    class Meta:
        unique_together = ('dept_school', 'academic_year')

    def __str__(self):
        return f"{self.dept_school} ({self.academic_year})"


class SpecialAssistantProgram(models.Model):
    STATUS_CHOICES = [
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
    ]

    academic_audit = models.ForeignKey(
        AcademicAudit,
        on_delete=models.CASCADE,
        related_name='special_programs'
    )
    name_of_prog = models.CharField(max_length=255)
    year_of_recognition = models.PositiveIntegerField()
    duration = models.CharField(max_length=50)  # e.g., "2 years"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.name_of_prog} ({self.status})"
