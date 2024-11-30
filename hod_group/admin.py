from django.contrib import admin
from .models import StudentAdmitted

@admin.register(StudentAdmitted)
class StudentAdmittedAdmin(admin.ModelAdmin):
    list_display = ('dept_name', 'prog_name', 'teacher', 'acad_year', 'admit_seats')
    search_fields = ('dept_name', 'prog_name__program', 'teacher__name')
    list_filter = ('acad_year', 'prog_name')
