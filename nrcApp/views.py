from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import Customer, PartyDetail, Invoice, ProductLine
from teachers.models import Teacher, Department
from django.core.signing import Signer, BadSignature
from django.http import JsonResponse
from django.template.loader import render_to_string
import re
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
import json
from weasyprint import HTML, CSS
import os
from django.urls import reverse
from .forms import (
    CustomerForm,
    PartyDetailForm,
    InvoiceForm,
    ProductLineFormSet,   
    ResearchUploadForm
)
from django.db.models import Q
import django_filters
#from .filters import CustomerFilter
import pandas as pd
import openpyxl
from .forms import ExcelUploadForm
from decimal import Decimal, InvalidOperation

# Create your views here.

def home(request):
    return render(request, 'teachers/home1.html')
    
@login_required
def group_table(request):   
    return render(request, "nrcApp/group_table.html")
    
    
@login_required
def group_table_with_id(request, group_id):
    # Get the currently logged-in user
    user = request.user
    
    # Fetch the Teacher instance associated with the user
    teacher = get_object_or_404(Teacher, user=user)
    programs = Department.objects.filter(name=teacher.dept_name)
    # Filter students based on the teacher's department name
    #students = StudentAdmitted.objects.select_related('teacher', 'prog_name').filter(dept_name=teacher.dept_name)
    
    #courses = OnlineCourse.objects.select_related('teacher',).filter(dept_name=teacher.dept_name)
    #customers = Customer.objects.all()
    #customers = Customer.objects.filter(created_at__date=localdate()).order_by('-created_at')
    customers = Customer.objects.all().order_by('-updated_date')
    invoices = Invoice.objects.all().order_by('-date')
    #researches = ResearchProject.objects.all()
    
    # Define a mapping of group IDs to their respective templates
    group_templates = {
        'group1': 'nrcApp/group1a_details.html',
        'group2': 'nrcApp/group2_details.html',
        'group3': 'nrcApp/invoice_list.html',
        'group4': 'nrcApp/group4_details.html',
    }

    #template = group_templates.get(group_id)
    template = group_templates.get(group_id)
    
    # Reverse lookup to find the key (group_id) from the template
    grp_id = next((key for key, value in group_templates.items() if value == template), None)
    request.session['grp_id'] = grp_id
    group_id = grp_id    
    #if request.session['grp_id'] == 'group1':
    #   form = StudentAdmittedForm(programs=programs)
    #   success = request.session.get('success', None)      
    #else:
    #   form=""
    #  success=""
    
    # Initialize `form` and `success`
    form = None
    success = request.session.get('success', None)
    
    # Assign forms based on the group ID
    if grp_id == 'group1':
        form = CustomerForm()
    elif grp_id == 'group3':
        form = InvoiceForm()
    #elif grp_id == 'group4':
        #form = ResearchProjectForm()
    else:
        form=""
        success=""
    
    
    # Clear the success session variable
    if 'success' in request.session:
        del request.session['success']
        
    # Handle success session
    #success = request.session.get('success', False)
    #if 'success' in request.session:
    #    del request.session['success']  # Remove the success session variable
  
       
    # Optionally pass additional context
    # Pass context to the template
    context = {
        'group_id': group_id,
        'grp_id': grp_id,
        #'students': students,
        #'courses': courses,
        'customers':customers,
        'invoices': invoices,
        #'researches': researches,
        'form': form,
        'success': success,
        'party_detail_url': reverse('nrcApp:party_detail_list')
        
    }
   
    return render(request, template, context)

@login_required
def customer_add(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)
    
    #programs = Department.objects.filter(name=teacher.dept_name)
    success = False
    request.session['success'] = success
    
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.dept_name = teacher.dept_name
            customer.teacher_id = teacher.id            
            customer.group_id = request.session.get('grp_id', None)
            customer.save()
            success = True
            request.session['success'] = success
            
            
            # For non-AJAX requests, redirect
            return redirect('nrcApp:group_table_with_id', group_id=customer.group_id)
        else:
            print(form.errors)  # Debugging: Print errors to console

    else:
        form = CustomerForm()
    
    return render(request, 'nrcApp/group1a_details.html', 
                 {'form': form, 'grp_id': request.session.get('grp_id', None)})

@login_required
def customer_add_continue(request):
    
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = request.user
        teacher = get_object_or_404(Teacher, user=user)
        form = CustomerForm(request.POST, request.FILES)
        
        if form.is_valid():
            customer = form.save(commit=False)
            customer.dept_name = teacher.dept_name
            customer.teacher_id = teacher.id            
            customer.group_id = request.session.get('grp_id', None)
            customer.save()
            success = True
            request.session['success'] = success            
            
            return JsonResponse({'success': True, 'message': 'Record added successfully!'})
            
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': json.loads(errors)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
    

                 
@login_required
def edit_customer(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)    
    if request.method == "POST":
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "Customer updated successfully!")
            return redirect('nrcApp:group_table_with_id', group_id=customer.group_id)
    else:
        form = OnlineCourseForm(instance=course)

    return render(request, "nrcApp/group1a_details.html", {"form": form})


@login_required
def customer_delete(request, signed_id):
    # Initialize the signer
    signer = Signer()

    try:
        # Unsign the token to get the original ID
        id = signer.unsign(signed_id)
        # Get the qualification object ensuring it belongs to the current user
        #qualification = get_object_or_404(Qualification, id=id, teacher__user=request.user)
        customer = get_object_or_404(Customer, id=id)
        grp_id = customer.group_id
    except BadSignature:
        # If the token is invalid, deny access
        #return HttpResponseForbidden("<h2>Invalid request. Go back</h2>")
        return render(request, 'teachers/403.html', status=403)
    
    if request.method == 'POST':
         
        # Delete the student object
        customer.delete()
        
        # Redirect to the group_table_with_id view with the group_id
        return redirect('nrcApp:group_table_with_id', group_id=grp_id)
    
    
    return render(request, 'nrcApp/course_confirm_delete.html', {'customer': customer, 'grp_id': grp_id, 'signed_id': signed_id})


@login_required
def customer_view_pdf(request, signed_id):
    signer = Signer()
    try:
        id = signer.unsign(signed_id)
        customer = get_object_or_404(Customer, id=id)
        grp_id = customer.group_id
    except Customer.DoesNotExist:
        return HttpResponse("Customer not found", status=404)

    # Get related party details
    bill_to = customer.party_details.filter(party_type='BILL_TO').first()
    ship_to = customer.party_details.filter(party_type='SHIP_TO').first()

    html_string = render_to_string('nrcApp/customer_pdf_template.html', {
        'customer': customer,
        'bill_to': bill_to,
        'ship_to': ship_to,
    })
    html = HTML(string=html_string)
    pdf_file = html.write_pdf()

    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="customer_details.pdf"'
    return response
    
    
def party_detail_list(request):
    parties = PartyDetail.objects.all()
    group_id = request.session.get('grp_id')
    return render(request, 'nrcApp/party_detail_list.html', {'parties': parties,'group_id': group_id})

def party_detail_create(request):
    if request.method == 'POST':
        form = PartyDetailForm(request.POST)        
        if form.is_valid():
            party = form.save(commit=False)
            party.party_code = ""
            if party.party_type == "BILL_TO":
                party.party_code = "B001"
            elif party.party_type == "SHIP_TO":
                party.party_code = "S001"            
            party.save()
            return redirect('nrcApp:party_detail_list')
    else:
        form = PartyDetailForm()
    return render(request, 'nrcApp/party_detail_form.html', {'form': form})
    
def party_detail_update(request, pk):
    party = get_object_or_404(PartyDetail, pk=pk)
    if request.method == 'POST':
        form = PartyDetailForm(request.POST, instance=party)
        if form.is_valid():
            party = form.save(commit=False)
            party.party_code = ""
            if party.party_type == "BILL_TO":
                party.party_code = "B001"
            elif party.party_type == "SHIP_TO":
                party.party_code = "S001" 
            party.save()
            return redirect('nrcApp:party_detail_list')
    else:
        form = PartyDetailForm(instance=party)
    return render(request, 'nrcApp/party_detail_form.html', {'form': form})

def party_detail_delete(request, pk):
    party = get_object_or_404(PartyDetail, pk=pk)
    if request.method == 'POST':
        party.delete()
        return redirect('nrcApp:party_detail_list')
    return render(request, 'nrcApp/party_detail_confirm_delete.html', {'party': party})


@login_required
def invoice_list(request):
    invoices = Invoice.objects.all().order_by('-date')
    return render(request, 'nrcApp/invoice_list.html', {'invoices': invoices})



@login_required
def invoice_create(request):
    if request.method == 'POST':
        customer_id = request.POST.get('customer')

        form = InvoiceForm(request.POST)
        # Inject party choices dynamically into form
        if customer_id:
            bill_parties = PartyDetail.objects.filter(customer_id=customer_id, party_type='BILL_TO')
            ship_parties = PartyDetail.objects.filter(customer_id=customer_id, party_type='SHIP_TO')
            form.fields['bill_to_party'].queryset = bill_parties
            form.fields['ship_to_party'].queryset = ship_parties

        if form.is_valid():
            invoice = form.save()
            formset = ProductLineFormSet(request.POST, instance=invoice)

            if formset.is_valid():
                formset.save()
                return redirect('nrcApp:invoice_list')
            else:
                print("Formset errors:", formset.errors)
        else:
            print("Form errors:", form.errors)
            formset = ProductLineFormSet(request.POST)
    else:
        form = InvoiceForm()
        formset = ProductLineFormSet()

    # Show dropdown options for first render
    selected_customer_id = request.GET.get('customer_id') or form.initial.get('customer')
    bill_to_parties = PartyDetail.objects.none()
    ship_to_parties = PartyDetail.objects.none()

    if selected_customer_id:
        bill_to_parties = PartyDetail.objects.filter(customer_id=selected_customer_id, party_type='BILL_TO')
        ship_to_parties = PartyDetail.objects.filter(customer_id=selected_customer_id, party_type='SHIP_TO')
        form.fields['bill_to_party'].queryset = bill_to_parties
        form.fields['ship_to_party'].queryset = ship_to_parties

    return render(request, 'nrcApp/invoice_form.html', {
        'form': form,
        'formset': formset,
        'bill_to_parties': bill_to_parties,
        'ship_to_parties': ship_to_parties,
    })

@login_required
def invoice_edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)

    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        
        # Dynamically update queryset for party fields
        customer_id = request.POST.get('customer')
        if customer_id:
            form.fields['bill_to_party'].queryset = PartyDetail.objects.filter(customer_id=customer_id, party_type='BILL_TO')
            form.fields['ship_to_party'].queryset = PartyDetail.objects.filter(customer_id=customer_id, party_type='SHIP_TO')

        formset = ProductLineFormSet(request.POST, instance=invoice)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            return redirect('nrcApp:invoice_list')
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        form = InvoiceForm(instance=invoice)
        formset = ProductLineFormSet(instance=invoice)

        customer_id = invoice.customer_id
        form.fields['bill_to_party'].queryset = PartyDetail.objects.filter(customer_id=customer_id, party_type='BILL_TO')
        form.fields['ship_to_party'].queryset = PartyDetail.objects.filter(customer_id=customer_id, party_type='SHIP_TO')

    return render(request, 'nrcApp/invoice_form.html', {
        'form': form,
        'formset': formset
    })


@login_required
def invoice_delete(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    invoice.delete()
    return redirect('nrcApp:invoice_list')
    
@login_required
def get_party_details(request):
    customer_id = request.GET.get('customer_id')
    data = {'bill_to': [], 'ship_to': []}

    if customer_id:
        bill_to = PartyDetail.objects.filter(customer_id=customer_id, party_type='BILL_TO')
        ship_to = PartyDetail.objects.filter(customer_id=customer_id, party_type='SHIP_TO')

        data['bill_to'] = [{'id': p.id, 'name': p.party_name} for p in bill_to]
        data['ship_to'] = [{'id': p.id, 'name': p.party_name} for p in ship_to]

    return JsonResponse(data)    

def upload_customers(request):
    grp_id = "group1"
    
    if request.method == 'POST':
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            # Validate O1 cell
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            o1_value = ws["O1"].value
            excel_file.seek(0)

            if str(o1_value).strip() != "123":
                form.add_error('file', "Invalid template: Secret code mismatch in cell O1.")
                return render(request, 'nrcApp/upload_customers.html', {'form': form})

            df = pd.read_excel(excel_file)

            for _, row in df.iterrows():
                if pd.notna(row.get('customer_code')) and pd.notna(row.get('customer_name')):
                    Customer.objects.update_or_create(
                        customer_code=row['customer_code'],
                        defaults={
                            'customer_name': row['customer_name'],
                            'address': row.get('address', ''),
                            'city': row.get('city', ''),
                            'state': row.get('state', ''),
                            'pincode': row.get('pincode', ''),
                            'country': row.get('country', 'India'),
                            'contact_person': row.get('contact_person', ''),
                            'phone': row.get('phone', ''),
                            'email': row.get('email', ''),
                            'gst_number': row.get('gst_number', ''),
                            'pan_number': row.get('pan_number', ''),
                            'credit_limit': row.get('credit_limit', 0.00),
                        }
                    )

            # ✅ Set session flag for message
            request.session['upload_success'] = True
            request.session['redirect_url'] = reverse('nrcApp:group_table_with_id', args=[grp_id])
            return redirect('nrcApp:upload_customers')  # Reload to avoid resubmission
    else:
        form = ExcelUploadForm()

    # ✅ Check and clean up message
    upload_success = request.session.pop('upload_success', False)
    redirect_url = request.session.pop('redirect_url', None)

    return render(request, 'nrcApp/upload_customers.html', {
        'form': form,
        'upload_success': upload_success,
        'redirect_url': redirect_url
    })


@login_required
def research_add_continue(request):    
    
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user = request.user
        teacher = get_object_or_404(Teacher, user=user)
        form = ResearchProjectForm(request.POST, request.FILES)
        
        if form.is_valid():
            research = form.save(commit=False)
            researchr.dept_name = teacher.dept_name
            research.teacher_id = teacher.id            
            research.group_id = request.session.get('grp_id', None)
            research.save()
            success = True
            request.session['success'] = success            
            
            return JsonResponse({'success': True, 'message': 'Record added successfully!'})
            
        else:
            errors = form.errors.as_json()
            return JsonResponse({'success': False, 'errors': json.loads(errors)}, status=400)

    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

def safe_decimal(val, default=0.00):
    try:
        if pd.isna(val) or str(val).strip().lower() in ['nan', '', 'none']:
            return Decimal(default)
        return Decimal(str(val).strip())
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)


