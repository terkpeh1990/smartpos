from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Products


def manage_inventroy(request):
    
    inventory = Inventory.objects.all()

    template = 'restock/inventory.html'

    context = {
        'inventory': inventory,
        
    }

    return render(request,template,context)

