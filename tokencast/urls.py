from django.urls import path
from . import views

app_name = 'tokencast'

urlpatterns = [
    path('initiate/', views.initiate_poll, name='initiate_poll'),
    path('dashboard/', views.poll_dashboard, name='poll_dashboard'),   
    path('vote/<str:verification_code>/', views.cast_vote, name='cast_vote'),  # Change `uuid` to `str`    
    path('end_poll/<int:poll_id>/', views.end_poll, name='end_poll'),
    path('vote_success/', views.vote_success, name='vote_success'),
]
