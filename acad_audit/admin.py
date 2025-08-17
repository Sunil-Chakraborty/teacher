# acad_audit/admin.py
from django.contrib import admin
from django import forms
from django.db import models
from .models import AcademicAudit
from teachers.models import Department


class AcademicAuditAdminForm(forms.ModelForm):
    class Meta:
        model = AcademicAudit
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Keep all departments (we'll filter in JS)
        queryset = Department.objects.all().order_by('name')
        unique_ids = (
            queryset
            .values('name')
            .annotate(min_id=models.Min('id'))
            .values_list('min_id', flat=True)
        )
        self.fields['dept_school'].queryset = Department.objects.filter(id__in=unique_ids).order_by('name')

        # Add faculty info to widget choices
        choices_with_data = []
        for dept in self.fields['dept_school'].queryset:
            choices_with_data.append((dept.id, dept.name, dept.faculty))
        self.fields['dept_school'].widget.choices = [
            (dept.id, dept.name) for dept in self.fields['dept_school'].queryset
        ]
        # We'll use JS to attach the data attributes dynamically


@admin.register(AcademicAudit)
class AcademicAuditAdmin(admin.ModelAdmin):
    form = AcademicAuditAdminForm

    class Media:
        js = ('admin/js/faculty_filter.js',)
