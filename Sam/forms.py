from django import forms

from Sam.views import *
from .models import Item, Job, Receipt, Suppliers


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields ="__all__"

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields ="__all__"
class CustomerInvoiceForm(forms.ModelForm):
    class Meta:
        model = CustomerInvoice
        fields ="__all__"
class SupplierForm(forms.ModelForm):
    class Meta:
        model = Suppliers
        fields ="__all__"
