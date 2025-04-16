from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'hod_group'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    
    path('group_table/', views.group_table, name='group_table'),  # Without table_id    
    path('group-table/<str:group_id>/', views.group_table_with_id, name='group_table_with_id'),
    
    
    path('students/add/', views.student_add, name='student_add'),
    path('students/edit/<str:signed_id>/', views.student_edit, name='student_edit'),
    path('students/delete/<str:signed_id>/', views.student_delete, name='student_delete'),
    
    path('courses/add/', views.onlineCourse_add, name='courses_add'),
    path("edit_course/<int:course_id>/", views.edit_course, name="edit_course"),
    path('course/delete/<str:signed_id>/', views.course_delete, name='course_delete'),
    path('courses/add_continue/', views.onlineCourse_add_continue, name='courses_add_continue'),

    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
