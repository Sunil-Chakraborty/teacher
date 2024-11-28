from django.urls import path
from . import views


app_name = 'teachers'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    path('profile/edit/', views.edit_personal_details, name='edit_personal_details'),
    
    path('qualification/add/', views.add_qualification, name='add_qualification'),
    path('qualification/edit/<str:signed_id>/', views.edit_qualification, name='edit_qualification'),
    path('qualification/delete/<str:signed_id>/', views.delete_qualification, name='delete_qualification'),
    
    path('patents/', views.patent_list, name='patent_list'),
    path('patents/add/', views.add_patent, name='add_patent'),
    path('patents/edit/<int:pk>/', views.edit_patent, name='edit_patent'),
    path('patents/delete/<int:pk>/', views.delete_patent, name='delete_patent'),
    
    path('group-table/', views.group_table, name='group_table'),  # Without table_id    
    path('group-table/<str:group_id>/', views.group_table_with_id, name='group_table_with_id'),
    
]