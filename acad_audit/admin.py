from django.contrib import admin
from django import forms
from django.db import models
from .models import AcademicAudit
from teachers.models import Department


class AcademicAuditAdminForm(forms.ModelForm):
    class Meta:
        model = AcademicAudit
        fields = "__all__"

    def __init__(self, *args, faculty_selected=None, **kwargs):
        super().__init__(*args, **kwargs)

        # If editing existing record, use its faculty
        if self.instance and self.instance.pk:
            faculty_selected = self.instance.faculty

        if faculty_selected:
            queryset = Department.objects.filter(faculty=faculty_selected)

            # Unique names → keep lowest id per name
            unique_ids = (
                queryset.values("name")
                .annotate(min_id=models.Min("id"))
                .values_list("min_id", flat=True)
            )
            self.fields["dept_school"].queryset = Department.objects.filter(
                id__in=unique_ids
            ).order_by("name")
        else:
            self.fields["dept_school"].queryset = Department.objects.none()


@admin.register(AcademicAudit)
class AcademicAuditAdmin(admin.ModelAdmin):
    form = AcademicAuditAdminForm
    list_display = (
        'faculty',          # ✅ show faculty in list view
        'dept_school',
        'academic_year',
        'name_hod',
        'spl_assistant_prog',
    )
    list_filter = ('faculty', 'academic_year', 'spl_assistant_prog')  # ✅ quick filtering
    search_fields = ('dept_school__name', 'name_hod')  # ✅ search by dept or HOD name
    def get_form(self, request, obj=None, **kwargs):
        faculty_selected = request.GET.get("faculty")

        class PrefilledForm(self.form):
            def __init__(self, *args, **inner_kwargs):
                inner_kwargs["faculty_selected"] = faculty_selected
                super().__init__(*args, **inner_kwargs)

        kwargs["form"] = PrefilledForm
        return super().get_form(request, obj, **kwargs)

    class Media:
        js = ("admin/js/faculty_autosubmit.js",)
