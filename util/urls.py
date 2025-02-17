from django.conf import settings
from django.conf.urls.static import static

from django.urls import path
from .import views


app_name = 'util'

urlpatterns = [    
    path('upload/', views.upload_pdf_extract_links, name='upload_pdf_extract_links'),
    path('upload-links/', views.upload_links_and_download, name='upload_links'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)