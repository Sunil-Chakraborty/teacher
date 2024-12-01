from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import StudentAdmitted
from teachers.models import Teacher, Department

from .forms import StudentAdmittedForm

# Create your views here.

def home(request):
    return render(request, 'teachers/home.html')
    
@login_required
def group_table(request):   
    return render(request, "hod_group/group_table.html")
    
    
@login_required
def group_table_with_id(request, group_id):
    # Get the currently logged-in user
    user = request.user
    
    # Fetch the Teacher instance associated with the user
    teacher = get_object_or_404(Teacher, user=user)
    
    # Filter students based on the teacher's department name
    students = StudentAdmitted.objects.select_related('teacher', 'prog_name').filter(dept_name=teacher.dept_name)
    
    # Define a mapping of group IDs to their respective templates
    group_templates = {
        'group1': 'hod_group/group1_details.html',
        'group2': 'hod_group/group2_details.html',
        'group3': 'hod_group/group3_details.html',
    }

    # Get the corresponding template or use a default one
    #template = group_templates.get(group_id, 'default_group.html')
    
    template = group_templates.get(group_id)
    
    
    # Optionally pass additional context
    context = {'group_id': group_id, 'students':students}

    return render(request, template, context)
    

@login_required
def student_add(request):
    user = request.user
    # Fetch the Teacher instance associated with the user
    teacher = get_object_or_404(Teacher, user=user)
   
    if request.method == 'POST':
        # Pass the queryset of Department instances to the form
        programs = Department.objects.filter(name=teacher.dept_name)
        form = StudentAdmittedForm(request.POST, programs=programs)
        if form.is_valid():
            student = form.save(commit=False)
            student.dept_name = teacher.dept_name  # Assign dep_name from the teacher instance
            student.teacher_id = teacher.id       # Assign teacher_id from the teacher instance
            prog = Department.objects.get(pk=student.prog_name_id)
            student.prog_cd = prog.prog_cd
            student.course_name = prog.program
            
            student.save()
            return redirect('hod_group:group_table')  # Redirect to students list after adding a record
    else:
        programs = Department.objects.filter(name=teacher.dept_name)
        form = StudentAdmittedForm(programs=programs)

    return render(request, 'hod_group/student_add.html', {'form': form})

@login_required
def student_edit(request, pk):
    student = get_object_or_404(StudentAdmitted, pk=pk)
    if request.method == 'POST':
        form = StudentAdmittedForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('hod_group:group_table')
    else:
        form = StudentAdmittedForm(instance=student)
    return render(request, 'hod_group/student_edit.html', {'form': form})

@login_required
def student_delete(request, pk):
    student = get_object_or_404(StudentAdmitted, pk=pk)
    if request.method == 'POST':
        student.delete()
        return redirect('hod_group:group_table')
    return render(request, 'hod_group/student_confirm_delete.html', {'student': student})
    
