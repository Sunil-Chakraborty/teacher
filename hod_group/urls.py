from django.urls import path
from . import views


app_name = 'hod_group'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    
    path('group_table/', views.group_table, name='group_table'),  # Without table_id    
    path('group-table/<str:group_id>/', views.group_table_with_id, name='group_table_with_id'),
    
    
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<str:signed_id>/', views.student_edit, name='student_edit'),
    path('students/delete/<str:signed_id>/', views.student_delete, name='student_delete'),
    
   
]