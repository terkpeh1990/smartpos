from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

def manage_category(request):
    
    categorys = Category.objects.all()

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Category Saved')
            return redirect('products:manage_category')
    
    else:
        form = CategoryForm()

    template = 'products/category.html'

    context = {
        'categorys': categorys,
        'form':form,
    }

    return render(request,template,context)

def edit_category(request,pk):
    
    categorys = Category.objects.all()
    category = categorys.get(id=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST,instance=category)
        if form.is_valid():
            form.save()
            messages.success(request,'Category Updated')
            return redirect('products:manage_category')
    
    else:
        form = CategoryForm(instance=category)

    template = 'products/category.html'

    context = {
        'categorys': categorys,
        'form':form,
    }

    return render(request,template,context)


def delete_category(request,pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.success(request,'Category Deleted')
    return redirect('products:manage_category')