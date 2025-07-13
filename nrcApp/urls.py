from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

app_name = 'nrcApp'

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    
    path('group_table/', views.group_table, name='group_table'),  # Without table_id    
    path('group-table/<str:group_id>/', views.group_table_with_id, name='group_table_with_id'),
    
    path('customer/add/', views.customer_add, name='customer_add'),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name="edit_customer"),
    path('customer/delete/<str:signed_id>/', views.customer_delete, name='customer_delete'),
    path('customer/add_continue/', views.customer_add_continue, name='customer_add_continue'),
    #path('.well-known/appspecific/com.chrome.devtools.json', lambda request: JsonResponse({}, status=204))  
    path('customer/view/<str:signed_id>/', views.customer_view_pdf, name='customer_view_pdf'),

    path('party-details/', views.party_detail_list, name='party_detail_list'),
    path('party-details/create/', views.party_detail_create, name='party_detail_create'),
    path('party-details/update/<int:pk>/', views.party_detail_update, name='party_detail_update'),
    path('party-details/delete/<int:pk>/', views.party_detail_delete, name='party_detail_delete'),

    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/create/', views.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/edit/', views.invoice_edit, name='invoice_edit'),
    path('invoices/<int:pk>/delete/', views.invoice_delete, name='invoice_delete'),

    path('ajax/get-party-details/', views.get_party_details, name='get_party_details'),
    path('upload-customers/', views.upload_customers, name='upload_customers'),
    
    #path('research/add/', views.research_add, name='research_add'),
    #path('edit_research/<int:research_id>/', views.edit_research, name="edit_research"),
    #path('research/delete/<str:signed_id>/', views.research_delete, name='research_delete'),
    path('research/add_continue/', views.research_add_continue, name='research_add_continue'),
   
    #path('.well-known/appspecific/com.chrome.devtools.json', lambda request: JsonResponse({}, status=204))  
    #path('research/view/<str:signed_id>/', views.research_view_pdf, name='research_view_pdf'),



]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
