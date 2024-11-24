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
    path('qualification/edit/<int:id>/', views.edit_qualification, name='edit_qualification'),
    path('qualification/delete/<int:id>/', views.delete_qualification, name='delete_qualification'),
    path('publication/add/', views.add_publication, name='add_publication'),
    path('publication/edit/<int:id>/', views.edit_publication, name='edit_publication'),
    path('publication/delete/<int:id>/', views.delete_publication, name='delete_publication'),
    
    path('group-table/', views.group_table, name='group_table'),  # Without table_id    
    path('group-table/<str:group_id>/', views.group_table_with_id, name='group_table_with_id'),
    
]