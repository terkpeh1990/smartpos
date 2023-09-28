from django import forms
from django.forms import Form
from django.forms.widgets import NumberInput
from django.contrib.auth import authenticate,get_user_model
import datetime
from .import models


class RestockForm(forms.ModelForm):
    restock_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Select Production Date')
    
    class Meta:
        model = models.Restock
        fields = ('restock_date','shift')

 

class RestockDetailForm(forms.ModelForm):
    
    quantity_produced = forms.IntegerField(label=False)
    requisition = forms.ModelChoiceField(
         queryset=models.Requisition.objects.filter(status = 'Issued').order_by('-id'),label='Select Approved Raw Material')

    def clean(self, *args, **kwargs):
        quantity_produced = self.cleaned_data.get('quantity_produced')
      
        if quantity_produced <= 0:
            raise forms.ValidationError(
                {'quantity_produced': ["Quantity cannot be less than 1"]})
            
        return super(RestockDetailForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.Restock_details
        fields = ('quantity_produced','requisition')


class DamageForm(forms.ModelForm):
    damage_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Select Production Date')
    product = forms.ModelChoiceField(
         queryset=models.Products.objects.all().order_by('name'),label='Select Product')
    quantity = forms.IntegerField()
    sub_code =forms.ModelChoiceField(
         queryset=models.Sub_Accounts.objects.filter(code__tag='Expense').order_by('sub_description'))

    def clean(self, *args, **kwargs):
        quantity = self.cleaned_data.get('quantity')
      
        if quantity <= 0:
            raise forms.ValidationError(
                {'quantity': ["Quantity cannot be less than 1"]})
            
        return super(DamageForm, self).clean(*args, **kwargs)

    class Meta:
        model = models.Damages
        fields = ('damage_date','sub_code','product','quantity',)


class ReasonForm(forms.ModelForm):
    reason = forms.CharField(label='Why Did You Field To Meet Production Target ?')

    class Meta:
        model = models.Restock_history
        fields = ('reason',)