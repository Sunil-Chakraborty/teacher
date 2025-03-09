from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('create/', views.create_poll, name='create_poll'),   
    path('results/<str:token_no>/', views.results, name='results'),
    path('vote/<str:token_no>/', views.vote_poll, name='vote_poll'),  # ✅ Ensure this line exists
     
]
