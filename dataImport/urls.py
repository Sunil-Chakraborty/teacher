from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

app_name = 'dataImport'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    
    path('group_table/', views.group_table, name='group_table'),  # Without table_id    
    path('group-table/<str:group_id>/', views.group_table_with_id, name='group_table_with_id'),
    
    path('upload-research/', views.upload_research, name='upload_research'),
    path('research-projects/bulk-create/', views.research_project_bulk_create, name='research_project_bulk_create'),
    path('research_edit/<int:research_id>', views.research_edit, name='research_edit'),
    path('research/<int:pk>/delete/', views.research_delete, name='research_delete'),
   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
