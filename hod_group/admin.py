from django.contrib import admin
from .models import StudentAdmitted, OnlineCourse

@admin.register(StudentAdmitted)
class StudentAdmittedAdmin(admin.ModelAdmin):
    list_display = ('dept_name', 'prog_name', 'teacher', 'acad_year', 'admit_seats')
    search_fields = ('dept_name', 'prog_name__program', 'teacher__name')
    list_filter = ('acad_year', 'prog_name')

@admin.register(OnlineCourse)
class OnlineCourse(admin.ModelAdmin):
    list_display = ('dept_name', 'course_name', 'teacher', 'prog_cd', 'enrol_year', 'contact_hrs','enrol_students','complete_count')
    search_fields = ('dept_name','teacher__name')
    list_filter = ('dept_name',)
    

