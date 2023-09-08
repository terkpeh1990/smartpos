from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def manage_product(request):
    
    products = Products.objects.all()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Product Saved')
            return redirect('products:manage_product')
    
    else:
        form = ProductForm()

    template = 'products/product.html'

    context = {
        'products': products,
        'form':form,
    }

    return render(request,template,context)

def edit_product(request,pk):
    
    products = Products.objects.all()
    product = products.get(id=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,'Product Updated')
            return redirect('products:manage_product')
    
    else:
        form = ProductForm(instance=product)

    template = 'products/product.html'

    context = {
        'products': products,
        'form':form,
    }

    return render(request,template,context)


def delete_product(request,pk):
    product = Products.objects.get(id=pk)
    product.delete()
    messages.success(request,'Product Deleted')
    return redirect('products:manage_product')