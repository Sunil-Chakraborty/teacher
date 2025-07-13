from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.models import User
from django.conf import settings  # Import settings to access AUTH_USER_MODEL
from django.utils import timezone
from teachers.models import Teacher, Department
from django.urls import reverse
from django.db.models import UniqueConstraint
from django.core.exceptions import ValidationError

import os
import uuid

class Customer(models.Model):
    teacher = models.ForeignKey(
        "teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Assigned Teacher"
    )
    dept_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Department Name"
    )
    customer_code   = models.CharField(max_length=10, unique=True)
    customer_name   = models.CharField(max_length=100)
    address         = models.TextField(max_length=200, blank=True)
    city            = models.CharField(max_length=50, blank=True)
    state           = models.CharField(max_length=50, blank=True)
    pincode         = models.CharField(max_length=10, blank=True)
    country         = models.CharField(max_length=50, default='India')
    contact_person  = models.CharField(max_length=100, blank=True)
    phone           = models.CharField(max_length=15, blank=True)
    email           = models.EmailField(blank=True)
    gst_number      = models.CharField(max_length=20, blank=True)
    pan_number      = models.CharField(max_length=10, blank=True)
    credit_limit    = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    is_active       = models.BooleanField(default=True)
    group_id    = models.CharField(
        max_length=10,        
        verbose_name="Group Table index",
        null=True,
        blank=True
    )
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.customer_code} - {self.customer_name}"
        
        
class PartyDetail(models.Model):
    PARTY_TYPE_CHOICES = [
        ('BILL_TO', 'Bill To'),
        ('SHIP_TO', 'Ship To'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='party_details')
    party_type = models.CharField(max_length=10, choices=PARTY_TYPE_CHOICES)
    party_code = models.CharField(max_length=10, blank=True, null=True)
    party_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.party_type}: {self.party_name
        }" 
    
    class Meta:
        constraints = [
            UniqueConstraint(fields=['customer', 'party_type'], name='unique_customer_partytype')
        ] 
        
    def clean(self):
        if PartyDetail.objects.filter(customer=self.customer, party_type=self.party_type).exclude(pk=self.pk).exists():
            raise ValidationError("Party detail with this Customer and Party type already exists.")
        


class ProductMaster(models.Model):
    product_code = models.CharField(max_length=20, unique=True)
    product_name = models.CharField(max_length=100)
    belt_type = models.CharField(max_length=50, choices=[
        ('Steel Cord', 'Steel Cord'),
        ('Fabric', 'Fabric'),
    ])
    width_mm = models.PositiveIntegerField(help_text="Width in millimeters")
    thickness_mm = models.DecimalField(max_digits=5, decimal_places=2, help_text="Total thickness in mm")
    tensile_strength = models.CharField(max_length=50, help_text="e.g., ST1000, ST1250")
    cover_grade = models.CharField(max_length=50, help_text="e.g., M24, DIN X")
    construction = models.TextField(help_text="Description of construction and specifications")
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit price in INR or USD")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product_code} - {self.product_name}"


class Invoice(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    bill_to_party = models.ForeignKey(
        PartyDetail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='bill_to_invoices',
        limit_choices_to={'party_type': 'BILL_TO'}
    )
    ship_to_party = models.ForeignKey(
        PartyDetail,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ship_to_invoices',
        limit_choices_to={'party_type': 'SHIP_TO'}
    )
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f"Invoice #{self.id} - {self.customer.customer_code}"
        
class ProductLine(models.Model):
    invoice = models.ForeignKey(
        Invoice, 
        on_delete=models.CASCADE, 
        related_name='product_lines'
    )
    product_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    rate = models.DecimalField(max_digits=10, decimal_places=2)

    def total(self):
        return self.quantity * self.rate

    def __str__(self):
        return f"{self.product_name} (Qty: {self.quantity})"



"""
How related_name Works in Practice:
create records:
cust = Customer.objects.create(customer_code='C001', customer_name='Acme Corp')
PartyDetail.objects.create(customer=cust, party_type='BILL_TO', party_code='B001', party_name='Acme HQ')
PartyDetail.objects.create(customer=cust, party_type='SHIP_TO', party_code='S001', party_name='Acme Warehouse')        

Access from Customer side:
cust.party_details.all()

Without related_name
cust.partydetail_set.all()
- which is less readable and less semantic than cust.party_details.all().


class ResearchProject(models.Model):
    teacher = models.ForeignKey(
        "teachers.Teacher", on_delete=models.CASCADE, null=True, blank=True,
        verbose_name="Assigned Teacher"
    )
    dept_name = models.CharField(
        max_length=100, null=True, blank=True,
        verbose_name="Department Name"
    )
    pi_name = models.CharField(
        max_length=100,
        verbose_name="Name of the PI/Co-PI"
    )
    project_title = models.TextField(
        verbose_name="Title of the Research Project"
    )
    funding_agency = models.CharField(
        max_length=100,
        verbose_name="Name of the Funding Agency"
    )
    award_year = models.CharField(
        max_length=9,
        verbose_name="Year of Award or Sanction",
        help_text="Format: YYYY-YY (e.g., 2018-19)"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Amount in Rs."
    )
    duration = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name="Duration (in years)"
    )
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_date    = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.pi_name} - {self.project_title[:40]}..."


"""