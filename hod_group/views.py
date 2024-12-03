from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import StudentAdmitted
from teachers.models import Teacher, Department
from django.core.signing import Signer, BadSignature

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

    #template = group_templates.get(group_id)
    template = group_templates.get(group_id)
    
    # Reverse lookup to find the key (group_id) from the template
    grp_id = next((key for key, value in group_templates.items() if value == template), None)
    request.session['grp_id'] = grp_id
    
    # Optionally pass additional context
    context = {'group_id': group_id, 'grp_id':grp_id, 'students':students}

    return render(request, template, context)
    

@login_required
def student_add(request):
    user = request.user
    # Fetch the Teacher instance associated with the user
    teacher = get_object_or_404(Teacher, user=user)
    grp_id = request.session.get('grp_id', None)
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
            
            # Retrieve grp_id from session
            student.group_id = request.session.get('grp_id', None)          
            
            student.save()
            #return redirect('hod_group:group_table')  # Redirect to students list after adding a record
            return redirect('hod_group:group_table_with_id', group_id=student.group_id)
    
    
    else:
        programs = Department.objects.filter(name=teacher.dept_name)
        form = StudentAdmittedForm(programs=programs)

    return render(request, 'hod_group/student_add.html', {'form': form, 'grp_id': grp_id })

@login_required
def student_edit(request, signed_id):
    # Initialize the signer
    signer = Signer()
    
    try:
        # Unsign the token to get the original ID
        id = signer.unsign(signed_id)
        
        student = get_object_or_404(StudentAdmitted, id=id)
        # Fetch the Teacher object associated with the logged-in user
        teacher = get_object_or_404(Teacher, user=request.user)
        grp_id = request.session.get('grp_id', None)
        programs = Department.objects.filter(name=teacher.dept_name)
        # Capture the data_row from query parameters
        data_row = request.GET.get('data_row')
        print(data_row)
        if data_row is None:
            return HttpResponseBadRequest("Missing data_row parameter.")
            
    except BadSignature:
    
        # If the token is invalid, deny access
        #return HttpResponseForbidden("Invalid request.")
        return render(request, 'teachers/403.html', status=403)

    if request.method == 'POST':
        form = StudentAdmittedForm(request.POST, instance=student, programs=programs)
        if form.is_valid():
            form.save()
            return redirect('hod_group:group_table_with_id', group_id=student.group_id)
    else:
        form = StudentAdmittedForm(instance=student, programs=programs)

    return render(request, 'hod_group/student_edit.html', {
        'form': form,
        'grp_id': grp_id,
        'programs': programs,
        'signed_id': signed_id,
        'data_row': data_row,  # Pass data_row to the template
    })
    
@login_required
def student_delete(request, signed_id):
    # Initialize the signer
    signer = Signer()

    try:
        # Unsign the token to get the original ID
        id = signer.unsign(signed_id)
        # Get the qualification object ensuring it belongs to the current user
        #qualification = get_object_or_404(Qualification, id=id, teacher__user=request.user)
        student = get_object_or_404(StudentAdmitted, id=id)
        grp_id = student.group_id
    except BadSignature:
        # If the token is invalid, deny access
        #return HttpResponseForbidden("<h2>Invalid request. Go back</h2>")
        return render(request, 'teachers/403.html', status=403)
    
    if request.method == 'POST':
         
        # Delete the student object
        student.delete()
        
        # Redirect to the group_table_with_id view with the group_id
        return redirect('hod_group:group_table_with_id', group_id=grp_id)
    
    
    return render(request, 'hod_group/student_confirm_delete.html', {'student': student, 'grp_id': grp_id, 'signed_id': signed_id})
