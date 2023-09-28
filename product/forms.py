from django import forms
from django.forms import Form
from django.forms.widgets import NumberInput
from django.contrib.auth import authenticate,get_user_model
import datetime
from .models import *

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = Category
        fields = '__all__'


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = Products
        exclude = ('id',)

class RawForm(forms.ModelForm):
    
    class Meta:
        model = RawMaterial
        exclude = ('id',)

class RestockForm(forms.ModelForm):
       
    restock_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label="Select Date")
    
    class Meta:
        model = Restocks
        fields = ('restock_date',)

    


class RestockDetailForm(forms.ModelForm):
    material_id = forms.ModelChoiceField(
         queryset=RawMaterial.objects.all().order_by('name'),label='Select Roll')
    class Meta:
        model = Restock_details
        fields = ('material_id','quantity',)

class RequisitionForm(forms.ModelForm):
       
    requisition_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label="Select Date")
    
    class Meta:
        model = Requisition
        fields = ('requisition_date',)

class RequisitionDetailForm(forms.ModelForm):
    material_id = forms.ModelChoiceField(
         queryset=RawMaterial.objects.all().order_by('name'),label='Select Roll')
    class Meta:
        model = Requisition_Details
        fields = ('material_id','quantity',)

class QuantityForm(forms.ModelForm):
    quantity_approved = forms.IntegerField(label=False)
    def clean(self, *args, **kwargs):
        quantity_approved = self.cleaned_data.get('quantity_approved')
        if quantity_approved < 1:
            
            raise forms.ValidationError(
                    {'quantity_approved': ["Quantity Approved Cannot Be Less Than 1"]})
        return super(QuantityForm, self).clean(*args, **kwargs)
    class Meta:
        model = Requisition_Details
        fields = ('quantity_approved',)
