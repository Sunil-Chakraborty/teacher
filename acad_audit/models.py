from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from teachers.models import Department
import re

def validate_academic_year(value):
    """
    Validate academic year format:
    - Must be YYYY-YY or YYYY–YY
    - Second year must equal first year + 1
    """
    # Accept YYYY-YY or YYYY–YY
    match = re.match(r'^(\d{4})[-–](\d{2})$', value)
    if not match:
        raise ValidationError("Academic year must be in format YYYY–YY or YYYY-YY (e.g., 2024–25)")

    start_year = int(match.group(1))
    end_suffix = int(match.group(2))

    expected_suffix = (start_year + 1) % 100  # last 2 digits of next year
    if end_suffix != expected_suffix:
        raise ValidationError(
            f"Invalid academic year: {value}. "
            f"The second year should be {start_year + 1} (e.g., {start_year}-{expected_suffix:02d})"
        )


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
        validators=[validate_academic_year],
    )
    spl_assistant_prog = models.BooleanField(default=False)

    class Meta:
        unique_together = ('dept_school', 'academic_year')

    def __str__(self):
        return f"{self.dept_school} ({self.academic_year})"

    def clean(self):
        """
        Auto-format academic_year before validation.
        Example:
        - 2024-2025 → 2024-25
        - 2024–2025 → 2024–25
        """
        if self.academic_year:
            # Replace en dash with hyphen for processing
            year_str = self.academic_year.replace("–", "-")

            # Match YYYY-YYYY
            match = re.match(r'^(\d{4})[-–](\d{4})$', year_str)
            if match:
                start_year = int(match.group(1))
                end_year = int(match.group(2))

                if end_year == start_year + 1:
                    # Convert to short format YYYY-YY
                    short_format = f"{start_year}-{str(end_year)[-2:]}"
                    # Preserve en dash if originally present
                    if "–" in self.academic_year:
                        short_format = short_format.replace("-", "–")
                    self.academic_year = short_format

        # Run validation
        super().clean()

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
