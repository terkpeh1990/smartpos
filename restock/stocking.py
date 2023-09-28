from django.shortcuts import render, redirect
import restock
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Products
from auth_accounts.models import Profile
from django.db.models import Sum
# Create your views here.

def manage_restock(request):
    
    restocks = Restock.objects.all()

    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            stock=form.save()
            messages.success(request,'Category Saved')
            return redirect('production:add_stock',stock.id)
    
    else:
        form = RestockForm()

    template = 'restock/restock.html'

    context = {
        'restocks': restocks,
        'form':form,
    }

    return render(request,template,context)

def add_stock(request,pk):
    products = Products.objects.all() 
    profiles = Profile.objects.filter(is_standard=True)

    try:
        daily_restock = Restock.objects.get(id=pk)
    except Restock.DoesNotExist:
        pass

    try:
        daily_restock_details = Restock_details.objects.filter(restock=daily_restock)
        if daily_restock_details:
            total = daily_restock_details.aggregate(cc=Sum('wages'))
            daily_restock.total_wages = total['cc']
            daily_restock.save()
        else:
            total = 0.00
            daily_restock.total_wages = total
            daily_restock.save()
    except Restock_details.DoesNotExist:
        pass

    if request.method == 'POST':
        form = RestockDetailForm(request.POST)

        product  = request.POST.get("product")
        profile = request.POST.get("profile")
        
        if form.is_valid():
            userprofile = Profile.objects.get(profile_code=profile)
            item = Products.objects.get(name=product) 
            qty =form.cleaned_data.get('quantity_produced')
            requisition =form.cleaned_data.get('requisition')
            try:
                item_in_inventory = Inventory.objects.get(product=item)
            except Inventory.DoesNotExist:
                item_in_inventory=Inventory.objects.create(product=item,instock=qty,unit_price=item.unit_price)

            
            if Restock_details.objects.filter(restock=daily_restock,profile=userprofile):
                user_production = Restock_details.objects.get(restock=daily_restock,profile=userprofile)
                user_production.quantity_produced+=qty
                user_production.requisition =requisition
                user_production.save()
                
                item_in_inventory.instock+=qty
                item_in_inventory.save()
                # Restock_history.objects.create(restock_detail=user_production,product=item,profile=userprofile,quantity=qty)
                messages.success(request,"Production added")
                return redirect('production:add_stock',daily_restock.id)
            else:
                user_production=Restock_details.objects.create(restock=daily_restock,product=item,profile=userprofile,quantity_produced=qty,requisition=requisition)
                
                # Restock_history.objects.create(restock_detail=user_production,product=item,profile=userprofile,quantity=qty)
                item_in_inventory.instock+=qty
                item_in_inventory.save()
                messages.success(request,"Production added")
                return redirect('production:add_stock',daily_restock.id)
    else:
        form = RestockDetailForm()
    template='restock/add_stock.html'
    context ={
        'products':products,
        'profiles':profiles,
        'daily_restock_details':daily_restock_details,
        'daily_restock':daily_restock,
        'form':form,

    }
    return render(request,template,context)



def edit_restock(request,pk):
    
    restocks = Restock.objects.all()
    restock = restocks.get(id=pk)
    if request.method == 'POST':
        form = RestockForm(request.POST,instance=restock)
        if form.is_valid():
            form.save()
            messages.success(request,'Production Updated')
            return redirect('production:manage_restock')
    
    else:
        form = RestockForm(instance=restock)

    template = 'products/category.html'

    context = {
        'restocks': restocks,
        'form':form,
    }

    return render(request,template,context)


def delete_restock(request,pk):
    restock = Restock.objects.get(id=pk)
    restock.delete()
    messages.success(request,'Production Deleted')
    return redirect('production:manage_restock')



def item_production_history(request,pk):
    
    restocks = Restock_details.objects.get(id = pk)
    history = Restock_history.objects.filter(restock_detail=restocks.id)

    if request.method == 'POST':
        form = ReasonForm(request.POST)
        if form.is_valid():
            cc = form.save(commit = False)
            cc.restock_detail = restocks
            cc.save()
            messages.success(request,'Reason Saved')
            return redirect('production:item_production_history', restocks.id )
    
    else:
        form = ReasonForm()

    template = 'restock/item_production_history.html'

    context = {
        'restocks': restocks,
        'history':history,
        'form':form
    }

    return render(request,template,context)


def edit_item_production_history(request,pk):
    item = Restock_history.objects.get(id=pk)
    restocks = Restock_details.objects.get(id = item.restock_detail.id)
    history = Restock_history.objects.filter(restock_detail=restocks.id)

    if request.method == 'POST':
        form = ReasonForm(request.POST,instance=item)
        if form.is_valid():
            cc = form.save(commit = False)
            cc.restock_detail = restocks
            cc.save()
            messages.success(request,'Reason Updated')
            return redirect('production:item_production_history', restocks.id )
    
    else:
        form = ReasonForm(instance=item)

    template = 'restock/item_production_history.html'

    context = {
        'restocks': restocks,
        'history':history,
        'form':form
    }

    return render(request,template,context)