from django.urls import path
from . import views


app_name = 'iqac'

urlpatterns = [
    path('', views.home, name='home'),  # Home page

]