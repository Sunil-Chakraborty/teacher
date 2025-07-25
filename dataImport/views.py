from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from .models import ResearchProject
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
    ResearchProjectForm,
    ResearchUploadForm,
    ExcelUploadForm,
    ResearchProjectFormSet,
)
from django.db.models import Q
import django_filters
#from .filters import CustomerFilter
import pandas as pd
import openpyxl
from decimal import Decimal, InvalidOperation


# Create your views here.

def home(request):
    return render(request, 'teachers/home1.html')
    
@login_required
def group_table(request):   
    return render(request, "dataImport/group_table.html")
    
    
@login_required
def group_table_with_id(request, group_id):
    # Get the currently logged-in user
    user = request.user
    
    # Fetch the Teacher instance associated with the user
    teacher = get_object_or_404(Teacher, user=user)
    programs = Department.objects.filter(name=teacher.dept_name)
    
    researches = ResearchProject.objects.all()
    
    # Define a mapping of group IDs to their respective templates
    group_templates = {        
        'group4': 'dataImport/group4_details.html',
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
    if grp_id == 'group4':
        form = ResearchProjectForm()
    #elif grp_id == 'group3':
        #form = InvoiceForm()
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
        #'customers':customers,
        #'invoices': invoices,
        'researches': researches,
        'form': form,
        'success': success,
        #'party_detail_url': reverse('nrcApp:party_detail_list')
        
    }
   
    return render(request, template, context)


def safe_decimal(val, default=0.00):
    try:
        if pd.isna(val) or str(val).strip().lower() in ['nan', '', 'none']:
            return Decimal(default)
        return Decimal(str(val).strip())
    except (InvalidOperation, ValueError, TypeError):
        return Decimal(default)



@login_required
def upload_research(request):
    grp_id = "group4"

    try:
        teacher = Teacher.objects.get(user=request.user)
    except Teacher.DoesNotExist:
        return render(request, "dataImport/upload_research.html", {
            "form": ResearchUploadForm(),
            "upload_success": False,
            "error_message": "No teacher profile associated with this user."
        })

    if request.method == 'POST':
        form = ResearchUploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['file']

            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            o1_value = ws["O1"].value
            excel_file.seek(0)

            if str(o1_value).strip() != "123":
                form.add_error('file', "Invalid template: Secret code mismatch in cell O1.")
                return render(request, 'dataImport/upload_research.html', {'form': form})

            df = pd.read_excel(excel_file)
            print("Excel columns:", df.columns)

            for _, row in df.iterrows():
                if pd.notna(row.get('pi_name')) and pd.notna(row.get('project_title')) and pd.notna(row.get('amount')) and pd.notna(row.get('award_year')):
                    project, created = ResearchProject.objects.update_or_create(
                        pi_name=row['pi_name'],
                        project_title=row['project_title'],
                        award_year=row['award_year'],
                        amount=safe_decimal(row['amount']),
                        defaults={
                            'funding_agency': row.get('funding_agency', ''),
                            'duration': int(row.get('duration', 0)) if pd.notna(row.get('duration')) else 0,
                            'teacher': teacher,
                            'dept_name': teacher.dept_name,
                        }
                    )

            request.session['upload_success'] = True
            request.session['redirect_url'] = reverse('dataImport:group_table_with_id', args=[grp_id])
            return redirect('dataImport:upload_research')
    else:
        form = ResearchUploadForm()

    upload_success = request.session.pop('upload_success', False)
    redirect_url = request.session.pop('redirect_url', None)

    return render(request, 'dataImport/upload_research.html', {
        'form': form,
        'upload_success': upload_success,
        'redirect_url': redirect_url
    })

"""
Following Validation applied while adding data:
Skips empty or invalid rows.
Applies same rules as Excel upload.
Updates existing projects or creates new ones.
Associates each record with the logged-in teacher.
"""



@login_required
def research_project_bulk_create(request):
    user = request.user
    teacher = get_object_or_404(Teacher, user=user)

    if request.method == 'POST':
        formset = ResearchProjectFormSet(request.POST)

        valid_count = 0
        has_partial_error = False

        if formset.is_valid():
            for i, form in enumerate(formset.forms):
                if not form.has_changed():
                    continue  # skip blank forms

                # Extract required fields
                pi = form.cleaned_data.get('pi_name')
                title = form.cleaned_data.get('project_title')
                year = form.cleaned_data.get('award_year')
                amount = form.cleaned_data.get('amount')

                # Partial/incomplete row check
                if not all([pi, title, year, amount]):
                    form.add_error(None, "Please complete all required fields (PI, Title, Year, Amount).")
                    has_partial_error = True
                    print(f"❌ Row {i+1} is partially filled: {form.cleaned_data}")
                    continue

                # Save valid row
                ResearchProject.objects.update_or_create(
                    pi_name=pi,
                    project_title=title,
                    award_year=year,
                    amount=safe_decimal(amount),
                    defaults={
                        'funding_agency': form.cleaned_data.get('funding_agency', ''),
                        'duration': form.cleaned_data.get('duration', ''),
                        'teacher': teacher,
                        'dept_name': teacher.dept_name
                    }
                )
                valid_count += 1

            if has_partial_error:
                messages.error(request, "Some rows are incomplete. Please complete or clear them.")
            if valid_count > 0 and not has_partial_error:
                messages.success(request, f"{valid_count} project(s) saved.")
                return redirect('dataImport:group_table_with_id', 'group4')

            # ❗ If no valid rows and no partial error, stop redirect
            if valid_count == 0 and not has_partial_error:
                messages.warning(request, "No data submitted. Please enter research project details.")
        else:
            print("🔍 Formset is NOT valid at formset level:")
            for i, form in enumerate(formset):
                if form.errors:
                    print(f"Form {i+1} Errors:", form.errors)
            messages.error(request, "❌ Please correct the form errors.")

    else:
        formset = ResearchProjectFormSet(queryset=ResearchProject.objects.none())

    return render(request, 'dataImport/research_project_bulk_create.html', {
        'formset': formset
    })

    
@login_required
def research_edit(request, research_id):
    research = get_object_or_404(ResearchProject, id=research_id)
    if request.method == 'POST':
        form = ResearchProjectForm(request.POST, request.FILES, instance=research)
        if form.is_valid():
            form.save()
            messages.success(request, "Research rec updated successfully!")
            return redirect('dataImport:group_table_with_id', group_id="group4")
            
    else:
        form = ResearchProjectForm(instance=research)

    return render(request, 'dataImport/group4_details.html', {
        'form': form,
        'research': research
    })


    
@login_required
def research_delete(request, pk):
    research = get_object_or_404(ResearchProject, pk=pk)
    research.delete()
    return redirect('dataImport:group_table_with_id', 'group4')