from django import forms
from django.forms.widgets import NumberInput
from .import models


class OrderForm(forms.ModelForm):
    
    order_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}),label='Select Date')
    
    class Meta:
        model = models.Orders
        fields = ('order_date',)




class OrderDetailForm(forms.ModelForm):
  
    item = forms.ModelChoiceField(
         queryset=models.Products.objects.all().order_by('name'),label='Select Product')

    class Meta:
        model = models.Order_details
        fields = ('item','quantity',)



class SalesReturnDetailForm(forms.ModelForm):
      
    item = forms.ModelChoiceField(
         queryset=models.Products.objects.all().order_by('name'),label='Select Product')

    class Meta:
        model = models.Sales_return_details
        fields = ('item','quantity',)