from django import forms
from django.forms import Form
from django.forms.widgets import NumberInput
from django.contrib.auth import authenticate,get_user_model
import datetime
from .import models

class CategoryForm(forms.ModelForm):
    
    class Meta:
        model = models.Category
        fields = '__all__'


class ProductForm(forms.ModelForm):
    
    class Meta:
        model = models.Products
        exclude = ('id',)