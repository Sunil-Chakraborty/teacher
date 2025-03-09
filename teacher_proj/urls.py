# teacher_proj/urls.py
from django.urls import path, include, reverse
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/teachers/', permanent=False)),
    path('teachers/', include('teachers.urls', namespace='teachers')),
    path('iqac/', include('iqac.urls', namespace='iqac')),
    path('hod/', include('hod_group.urls', namespace='hod_group')),
    path('util/', include('util.urls', namespace='util')),
    path('polls/', include('polls.urls', namespace='polls')),
    path('tokencast/', include('tokencast.urls', namespace='tokencast')),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

