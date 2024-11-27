from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .models import CustomUser, Teacher, Qualification, Publication, Department
from django.contrib.auth.decorators import login_required
from .forms import UserRegistrationForm, TeacherForm, QualificationForm, PublicationForm # Import TeacherForm from forms.py
from django.http import JsonResponse
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
    if request.method == 'POST':
        form = QualificationForm(request.POST, request.FILES)
        if form.is_valid():
            qualification = form.save(commit=False)            
            qualification.teacher = get_object_or_404(Teacher, user=request.user)
            qualification.save()
            return redirect('teachers:profile')
    else:
        form = QualificationForm()
    return render(request, 'teachers/add_qualification.html', {'form': form})

@login_required
def edit_qualification(request, id):
    qualification = Qualification.objects.get(id=id, teacher__user=request.user)
    # print("Qualification ID:", qualification.id)
    if request.method == 'POST':
        form = QualificationForm(request.POST, request.FILES, instance=qualification)

        if form.is_valid():
            form.save()
            return redirect('teachers:profile')
    else:
        form = QualificationForm(instance=qualification)

    # Pass the qualification to the template
    return render(request, 'teachers/edit_qualification.html', {'form': form, 'qualification': qualification})

@login_required
def delete_qualification(request, id):
    qualification = Qualification.objects.get(id=id, teacher__user=request.user)
    if request.method == 'POST':
        qualification.delete()
        return redirect('teachers:profile')
    return render(request, 'teachers/confirm_delete.html', {'object': qualification})

# Similar functions for Publications...
@login_required
def add_publication(request):
    if request.method == 'POST':
        form = PublicationForm(request.POST)
        if form.is_valid():
            publication = form.save(commit=False)
            publication.teacher = Teacher.objects.get(user=request.user)
            publication.save()
            return redirect('teachers:profile')
    else:
        form = PublicationForm()
    return render(request, 'teachers/add_publication.html', {'form': form})

@login_required
def edit_publication(request, id):
    publication = Publication.objects.get(id=id, teacher__user=request.user)
    if request.method == 'POST':
        form = PublicationForm(request.POST, instance=publication)
        if form.is_valid():
            form.save()
            return redirect('teachers:profile')
    else:
        form = PublicationForm(instance=publication)
    return render(request, 'teachers/edit_publication.html', {'form': form, 'publication': publication})



@login_required
def delete_publication(request, id):
    publication = Publication.objects.get(id=id, teacher__user=request.user)
    if request.method == 'POST':
        publication.delete()
        return redirect('profile')
    return render(request, 'teachers/confirm_delete.html', {'object': publication})

@login_required
def group_table(request): 
    return render(request, 'teachers/group_table.html')
    
@login_required
def group_table_with_id(request, group_id):
    # Define a mapping of group IDs to their respective templates
    group_templates = {
        'group1': 'teachers/group1_details.html',
        'group2': 'teachers/group2_details.html',
        'group3': 'teachers/group3_details.html',
    }

    # Get the corresponding template or use a default one
    #template = group_templates.get(group_id, 'default_group.html')
    
    template = group_templates.get(group_id)
    
    
    # Optionally pass additional context
    context = {'group_id': group_id}

    return render(request, template, context)
    
    
