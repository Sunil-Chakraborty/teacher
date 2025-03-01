from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .import views


app_name = 'util'

urlpatterns = [    
    path('upload/', views.upload_pdf_extract_links, name='upload_pdf_extract_links'),
    path('upload-links/', views.upload_links_and_download, name='upload_links'),
    
    path("calculator/", views.calculator_view, name="calculator"),
    
    # Todo List app
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path('task/', views.task_list, name='task_list'),
    path('add/', views.add_task, name='add_task'),
    path('complete/<int:task_id>/', views.complete_task, name='complete_task'),
    path('delete/<int:task_id>/', views.delete_task, name='delete_task'),
    #path('edit/<int:task_id>/', views.edit_task, name='edit_task'),
    path("edit_task/<int:task_id>/<uuid:verification_code>/", views.edit_task, name="edit_task"),
    path('undo/<int:task_id>/', views.undo_task, name='undo_task'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

