from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
#from .models import Teacher, Qualification, Publication
from django.contrib.auth.decorators import login_required
#from .forms import UserRegistrationForm, TeacherForm, QualificationForm, PublicationForm # Import TeacherForm from forms.py


# Create your views here.


def home(request):    
    return render(request, 'iqac/home.html')