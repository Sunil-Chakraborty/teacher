from django.core.signing import Signer, BadSignature
from django.http import HttpResponseForbidden
from django.contrib import messages

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import(CustomUser, Teacher, Qualification,  Department, 
             Patents, ResearchPub)
from django.contrib.auth.decorators import login_required
from .forms import (UserRegistrationForm, TeacherForm, 
                   QualificationForm, PatentForm) 

from django.http import Http404                   
                   
#from django.db import connection
from django.db.models import F
from django.contrib.auth.models import Group

# Create your views here.


def home(request):
    return render(request, 'teachers/home.html')


def register(request):
    unique_departments = (
        Department.objects.values("name").distinct()
    )  # Only unique department names
    
    #form = UserRegistrationForm()
    form = UserRegistrationForm(initial={'emp_id': None, 'password': None})
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.department = form.cleaned_data["department"]  # This is now an instance
            user.save()
            form = UserRegistrationForm()  # Clear the form fields for new input
            login(request, user)
            return redirect("teachers:home")
    else:
        form = UserRegistrationForm(initial={'emp_id': None, 'password': None})

    return render(
        request, "teachers/register.html", {"form": form, "unique_departments": unique_departments}
    )
    
def login_view(request):
    hod_status=""
    dept=""
    user_name=""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            
            login(request, user)            
            
            dept = user.department  # Get the department object           
            user_name=user.first_name
            request.session['user_name'] = user_name
            
            # Store only the department name or ID in the session
            request.session['dept'] = dept.name if dept else None  # Storing department name
            
           
            # Check if the user is in the "iqac" group
            if user.groups.filter(name='iqac').exists():                
                return redirect('iqac:home')
                
            if user.groups.filter(name='hod').exists():
                hod_status = "Hod"  # Replace with your logic
                
            if user.groups.filter(name='actg_hod').exists():
                hod_status = "Actg_Hod"  # Replace with your logic
                
            request.session['hod'] = hod_status 
            
             
            # Otherwise, redirect to a default profile page or another page
            return redirect('teachers:profile')  # Replace with your desired default URL
            #return redirect(f"{reverse('teachers:profile')}?hod={hod}")
    
    else:
        form = AuthenticationForm()

    return render(request, 'teachers/login.html', {'form': form})
    
    
def logout_view(request):
    logout(request)
    return redirect('teachers:login')

@login_required
def profile(request):    
    try:
        department = Department.objects.get(id=request.user.department_id)  # Fetch the department instance
        department_name = department.name
    except Department.DoesNotExist:
        department_name = "Unknown"
    
    # Fetch the group name (assume the user belongs to one group, otherwise handle multiple)
    groups = request.user.groups.all()  # Fetch all groups for the user
    group_name = groups[0].name if groups else "No Group"  # Take the first group or default to "No Group"
    
    # Get or create the teacher instance
    teacher, created = Teacher.objects.update_or_create(
        user=request.user,
        defaults={
            'first_name': request.user.first_name,
            'dept_name': department_name,  # Pass the department name
            'emp_id': request.user.emp_id,
            'email': request.user.email,
            'group_name': group_name,  # Capture and pass the group name
        }
    )
   
    form = TeacherForm(instance=teacher)
    return render(request, 'teachers/profile.html', {'teacher': teacher, 'form': form})
    
    
    
@login_required
def edit_personal_details(request):
    user = request.user
    # Fetch the Teacher instance associated with the user
    teacher = get_object_or_404(Teacher, user=user)

    if request.method == 'POST':
        #print("POST Data:", request.POST)
        # Pass request.user to the form when initializing it
        form = TeacherForm(request.POST, request.FILES, instance=teacher, user=user)
        if form.is_valid():
            if 'clear' in form.cleaned_data and form.cleaned_data['clear']:
                instance.photo = None
            
            teacher = form.save(commit=False)
            teacher.user = request.user  # Associate with the current logged-in user
            teacher.save()
            return redirect('teachers:profile')
            
        else:
            # Print errors
            print("Form is invalid, errors: ", form.errors)
            return redirect(request.path)

    else:
        # Pass request.user to the form when initializing it for GET request
        form = TeacherForm(instance=teacher, user=user)

    return render(request, 'teachers/profile.html', {'form': form})

    
@login_required
def add_qualification(request):

    try:
        # Fetch the Teacher object associated with the logged-in user
        teacher = get_object_or_404(Teacher, user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not associated with a teacher profile.")
        return redirect('teachers:profile')  # Redirect if user has no teacher profile

    if request.method == 'POST':
        form = QualificationForm(request.POST, request.FILES)
        if form.is_valid():
            qualification = form.save(commit=False)            
            qualification.teacher = get_object_or_404(Teacher, user=request.user)
            qualification.dept_name = teacher.dept_name
            qualification.save()
            return redirect('teachers:profile')
    else:
        form = QualificationForm()
    return render(request, 'teachers/add_qualification.html', {'form': form})



@login_required
def edit_qualification(request, signed_id):
    # Initialize the signer
    signer = Signer()

    try:
        # Unsign the token to get the original ID
        id = signer.unsign(signed_id)
        # Get the qualification object ensuring it belongs to the current user
        qualification = get_object_or_404(Qualification, id=id, teacher__user=request.user)
        
        # Fetch the Teacher object associated with the logged-in user
        teacher = get_object_or_404(Teacher, user=request.user)
        
    except BadSignature:
        # If the token is invalid, deny access
        #return HttpResponseForbidden("Invalid request.")
        return render(request, 'teachers/403.html', status=403)

    # Handle form submission
    if request.method == 'POST':
        form = QualificationForm(request.POST, request.FILES, instance=qualification)
        if form.is_valid():
            qualification = form.save(commit=False)
            
            qualification.dept_name = teacher.dept_name
            qualification.save()            
            return redirect('teachers:profile')
        else:
            print("Error:", form.errors)
    else:
        form = QualificationForm(instance=qualification)

    # Render the edit template with the form
    return render(request, 'teachers/edit_qualification.html', {'form': form, 'qualification': qualification, 'signed_id': signed_id})

@login_required
def delete_qualification(request, signed_id):
 # Initialize the signer
    signer = Signer()

    try:
        # Unsign the token to get the original ID
        id = signer.unsign(signed_id)
        # Get the qualification object ensuring it belongs to the current user
        qualification = get_object_or_404(Qualification, id=id, teacher__user=request.user)
    except BadSignature:
        # If the token is invalid, deny access
        #return HttpResponseForbidden("<h2>Invalid request. Go back</h2>")
        return render(request, 'teachers/403.html', status=403)
        
    if request.method == 'POST':
        qualification.delete()
        return redirect('teachers:profile')
    return render(request, 'teachers/confirm_delete.html', {'object': qualification})

@login_required
def patent_list(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    patents = Patents.objects.filter(teacher=teacher)
    return render(request, 'teachers/patent_list.html', {'patents': patents})

@login_required
def add_patent(request):

    try:
        # Fetch the Teacher object associated with the logged-in user
        teacher = get_object_or_404(Teacher, user=request.user)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not associated with a teacher profile.")
        return redirect('teachers:patent_list')  # Redirect if user has no teacher profile

    if request.method == 'POST':
        form = PatentForm(request.POST, request.FILES)
        if form.is_valid():
            patent = form.save(commit=False)
            patent.teacher = get_object_or_404(Teacher, user=request.user)  # Associate the logged-in user with the patent
            
            # Check if title and status are empty
            if not patent.title or not patent.status:
                messages.error(request, "Title and Status cannot be empty.")
                #return redirect('teachers:profile')  # Redirect to profile
                return redirect(request.path)
                
            patent.dept_name = teacher.dept_name
            patent.save()
            return redirect('teachers:patent_list')
    else:
        form = PatentForm()
    return render(request, 'teachers/add_patent.html', {'form': form})


@login_required
def edit_patent(request, signed_id):

    # Initialize the signer
    signer = Signer()

    try:
        # Unsign the token to get the original ID
        id = signer.unsign(signed_id)
        # Get the qualification object ensuring it belongs to the current user
        patent = get_object_or_404(Patents, id=id, teacher__user=request.user)
        
        # Fetch the Teacher object associated with the logged-in user
        teacher = get_object_or_404(Teacher, user=request.user)
        
    except BadSignature:
        # If the token is invalid, deny access
        #return HttpResponseForbidden("Invalid request.")
        return render(request, 'teachers/403.html', status=403)

        
    if request.method == 'POST':
        form = PatentForm(request.POST, request.FILES, instance=patent)
        if form.is_valid():
            patent = form.save(commit=False)
            patent.dept_name = teacher.dept_name
            patent.save()
            messages.success(request, "Patent updated successfully.")
            return redirect('teachers:patent_list')
    else:
        form = PatentForm(instance=patent)

    return render(request, 'teachers/edit_patent.html', {'form': form})


@login_required
def delete_patent(request, pk):
    patent = get_object_or_404(Patents, pk=pk, teacher__user=request.user)
    
    if request.method == 'POST':
        patent.delete()
        messages.success(request, "Patent deleted successfully.")
        return redirect('teachers:patent_list')

    return render(request, 'teachers/confirm_delete_patent.html', {'patent': patent})

@login_required
def research_list(request):
    teacher = get_object_or_404(Teacher, user=request.user)
    
    researches = ResearchPub.objects.filter(teacher=teacher)
    return render(request, 'teachers/research_list.html', {'researches': researches})

