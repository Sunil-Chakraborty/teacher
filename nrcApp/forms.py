from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Customer, PartyDetail, Invoice, ProductLine
import re



class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ["customer_code", "customer_name", "address"]

    def clean_customer_code(self):
        code = self.cleaned_data.get('customer_code', '').strip()
        if not code:
            raise forms.ValidationError("Customer code is required.")
        # Must be 1 uppercase letter + 4 digits
        if not re.match(r'^[A-Z][0-9]{4}$', code):
            raise forms.ValidationError(
                "Customer code must start with a capital letter followed by exactly four digits (e.g. A1001)."
            )
        return code

    def clean_customer_name(self):
        name = self.cleaned_data.get('customer_name')
        if not name:
            raise forms.ValidationError("Customer name is required.")
        if any(char.isdigit() for char in name):
            raise forms.ValidationError("Customer name cannot contain numbers.")
        return name

    def clean_address(self):
        address = self.cleaned_data.get('address')
        if not address:
            raise forms.ValidationError("Address is required.")
        return address

    # Optional: Global clean
    def clean(self):
        cleaned_data = super().clean()
        code = cleaned_data.get('customer_code')
        name = cleaned_data.get('customer_name')
        
        if code and name and code.lower() == name.lower():
            raise forms.ValidationError("Customer code and name should not be the same.")


class PartyDetailForm(forms.ModelForm):
    class Meta:
        model = PartyDetail
        fields = ['customer', 'party_type', 'party_code', 'party_name', 'address']
        widgets = {
            'party_type': forms.Select(attrs={'class': 'form-select'}),
            'party_code': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'party_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'customer': forms.Select(attrs={'class': 'form-select'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Make 'customer' field read-only (disabled) during editing
        if self.instance and self.instance.pk:
            self.fields['customer'].disabled = True
            self.fields['party_code'].disabled = True
        else:
            # Creating: hide party_code field
            self.fields['party_code'].widget = forms.HiddenInput()


class ExcelUploadForm(forms.Form):
    file = forms.FileField(
        label='Upload Excel File',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx, .xls'
        })
    )
    
class ResearchUploadForm(forms.Form):
    file = forms.FileField(
        label='Upload Excel File',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.xlsx, .xls'
        })
    )

    
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['customer', 'bill_to_party', 'ship_to_party']

    def __init__(self, *args, **kwargs):
        customer = kwargs.pop('customer', None)
        super().__init__(*args, **kwargs)

        if customer:
            self.fields['bill_to_party'].queryset = PartyDetail.objects.filter(
                customer=customer, party_type='BILL_TO'
            )
            self.fields['ship_to_party'].queryset = PartyDetail.objects.filter(
                customer=customer, party_type='SHIP_TO'
            )
        else:
            self.fields['bill_to_party'].queryset = PartyDetail.objects.none()
            self.fields['ship_to_party'].queryset = PartyDetail.objects.none()

        self.fields['bill_to_party'].required = False
        self.fields['ship_to_party'].required = False
        
        # 👉 Make fields read-only during edit (i.e. when instance has a pk)
        if self.instance and self.instance.pk:
            self.fields['customer'].disabled = True
            self.fields['bill_to_party'].disabled = True
            self.fields['ship_to_party'].disabled = True

# Inline formset for ProductLine entries in the invoice
ProductLineFormSet = inlineformset_factory(
    parent_model=Invoice,
    model=ProductLine,
    fields=['product_name', 'quantity', 'rate'],
    extra=5,  # Number of empty rows for new products
    can_delete=True,
    widgets={
        'product_name': forms.TextInput(attrs={'class': 'form-control'}),
        'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        'rate': forms.NumberInput(attrs={'class': 'form-control'}),
    }
)






