from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from teachers.models import (CustomUser, Teacher, Qualification, 
     Department, Patents, ResearchPub)


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'emp_id', 'department', 'is_staff', 'is_superuser', 'get_groups']
    search_fields = ['email', 'first_name', 'last_name', 'emp_id']
    ordering = ['email']

    # Adding the groups to the form view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'emp_id', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Add 'groups' to the add/edit form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    # Custom method to display the groups as a comma-separated list
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Groups'

# Register the custom user admin
admin.site.register(CustomUser, CustomUserAdmin)


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = (         
        'email',        # Display the email from the associated CustomUser
        'gender', 
        'caste', 
        'designation', 
        'doj', 
        'exp', 
        'mobile', 
        'department'
    )  # Fields to display in the list view
    
    search_fields = ('mobile', 'user__email', 'department__name')  # Adjust search to query related fields
    list_filter = ('gender', 'caste', 'designation')  # Filters for filtering options
    ordering = ('-doj',)  # Order by date of joining, descending

    # Method to fetch email from the related CustomUser
    def email(self, obj):
        return obj.user.email if obj.user else "N/A"
    email.short_description = "Email"

    # Adjusted method to fetch department
    def department(self, obj):
        return obj.user.department.name if obj.user and obj.user.department else "N/A"
    department.short_description = "Department"
    
    
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'faculty', 'program')  # Fields to display in the list view
    search_fields = ('name', 'faculty', 'program')  # Fields to search
    list_filter = ('faculty',)  # Filters for filtering options
    
@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
	list_display = (
     'teacher','degree','subject','thesis','institution',
     'dt_award'
     )

@admin.register(Patents)
class PatentsAdmin(admin.ModelAdmin):
	list_display = (
     'inv_name','status','title','ref_no','dt_award','awarding_agency'
     )

@admin.register(ResearchPub)
class ResearchPubAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'authors_name',
        'jrnl_name',
        'yr_of_pub',
        'issn_no',
        'is_ugc_care',
    )
    search_fields = (
        'title_of_paper',
        'authors_name',
        'jrnl_name',
        'yr_of_pub',
        'issn_no',
    )
    list_filter = (
        'is_ugc_care',
        'yr_of_pub',
    )
