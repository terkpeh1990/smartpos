from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from .forms import *
from django.db.models import Count,Sum
from restock.models import Restock_details



def restock(request):
    restock_list = Restocks.objects.all()
    template = 'products/restock.html'
    context = {
        'restock_list': restock_list,
    }
    return render(request,template,context)

def add_restock(request):
    
    if request.method == 'POST':
        form = RestockForm(request.POST)
        if form.is_valid():
            restock = form.save()
            messages.info(request,'Restock Initiated, Please add Raw Materials')
            return redirect('products:add_restock_detail' , restock.id)
    else:
        form = RestockForm()

    template = 'products/createrestock.html'
    context = {
        'form':form,
        
    }
    return render(request,template,context)

def add_restock_detail(request,pk):
    restocks = Restocks.objects.get(id=pk)
    detail = Restock_details.objects.filter(restock_id=restocks.id)
    if detail:
        cal= detail.aggregate(cc=Sum('material_id__unit'))
        qt = detail.aggregate(cc=Sum('quantity'))
        total = cal['cc']
        tqt = qt['cc']
    else:
        total = 0
        tqt = 0

    if request.method == 'POST':
        form = RestockDetailForm(request.POST)
       
        if form.is_valid():
            restock = form.save(commit=False)
            restock.restock_id=restocks
            restock.save()
            return redirect('products:add_restock_detail' , restocks.id)
    else:
        form = RestockDetailForm()

    template = 'products/restock_detail.html'
    context = {
        'form':form,
        
        'detail':detail,
        'restock':restocks,
        'total':total,
        'tqt':tqt
       
    }
    return render(request,template,context)

def edit_restock_detail(request,pk):
    restocks = Restock_details.objects.get(id=pk)
    restock = Restocks.objects.get(id=restocks.restock_id.id)
    detail = Restock_details.objects.filter(restock_id=restock.id)
    if request.method == 'POST':
        form = RestockDetailForm(request.POST,instance=restocks)
        if form.is_valid():
            restockitem = form.save(commit=False)
            restockitem.restock_id =restock
            restockitem.save()
            messages.info(request,'Item Updated')
            return redirect('products:add_restock_detail' , restock.id)
    else:
        form = RestockDetailForm(instance=restocks)

    template = 'inventory/restock/update-restock-detail.html'
    context = {
        'form':form,
        
        'detail':detail,
        'restock':restock,
        
    }
    return render(request,template,context)


def delete_restock_item(request,pk):
    restock= Restock_details.objects.get(id=pk)
    restock.delete()
    messages.error(request,'Item Deleted')
    return redirect('products:add_restock_detail', restock_id)


def edit_restock(request,pk):
    restock = Restocks.objects.get(id=pk)
   
    if request.method == 'POST':
        form = RestockForm(request.POST,instance=restock)
        if form.is_valid():
            restock=form.save()
            
            messages.info(request,'Restock Updated')
            return redirect('products:add_restock_detail',restock.id)
    else:
        form = RestockForm(instance=restock)

    template = 'inventory/restock/create-restock.html'
    context = {
        'form':form,
        
    }
    return render(request,template,context)

def delete_restock(request,pk):
    restock = Restocks.objects.get(id=pk)
    restock.delete()
    messages.error(request,'Restock Deleted')
    return redirect('products:manage_restock')

def cancel_restock(request,pk):
    restock = Restocks.objects.get(id=pk)
    restock.status="Cancelled"
    restock.save()
    messages.error(request,'Restock Cancelled')
    return redirect('products:add_restock_detail',restock.id)

def reverse_restock(request,pk):
    restock = Restocks.objects.get(id=pk)
    restock.status="Pending"
    restock.save()
    messages.info(request,'Restock Transaction Reversed')
    return redirect('products:add_restock_detail',restock.id)

def approve_restock(request,pk):
    restock = Restocks.objects.get(id=pk)
    detail = Restock_details.objects.filter(restock_id=restock.id)
    for i in detail:
        try:
            inventory = RawMaterialInventory.objects.get(material_id = i.material_id.id)
            inventory.avialable_quantity += i.quantity
            inventory.save()
            Inventory_Details.objects.get_or_create(inventory_id = inventory,quantity_intake=i.quantity,expiring_date=restock.restock_date,batch_number=i.batch_number)
        except RawMaterialInventory.DoesNotExist:
            inventory = RawMaterialInventory.objects.create(material_id = i.material_id)
            inventory.avialable_quantity += i.quantity
            inventory.save()
            Inventory_Details.objects.get_or_create(inventory_id = inventory,quantity_intake=i.quantity,expiring_date=restock.restock_date,batch_number=i.batch_number)
    restock.status="Approved"
    restock.save()
    messages.info(request,'Restock Approved ')
    return redirect('products:add_restock_detail',restock.id)

def inventory(request):
    product_list =  RawMaterialInventory.objects.all()
    template = 'products/inventory.html'
    context = {
        'product_list': product_list,
        
    }
    return render(request,template,context)

def detail_inventory(request,pk):
    
    inventory =  RawMaterialInventory.objects.get(id=pk)
    product=RawMaterial.objects.get(id=inventory.material_id.id)
    inventory_detail = Inventory_Details.objects.filter(inventory_id=inventory.id)
    template = 'products/inventory_detail.html'
    context = {
        'inventory':inventory,
        'inventory_detail':inventory_detail,
        
    }
    return render(request,template,context)


def requisition(request):
    
    requisition_list = Requisition.objects.all()
    
    template = 'products/requisition.html'
    context = {
        'requisition_list': requisition_list,
        
       
    }
    return render(request,template,context)

def add_requisition(request):
    
    if request.method == 'POST':
        form = RequisitionForm(request.POST)
        if form.is_valid():
            requisition = form.save()
           
            messages.info(request,'Requisition Initiated, Please add Raw Material')
            return redirect('products:add_requisition_detail' , requisition.id)
    else:
        form = RequisitionForm()

    template = 'products/create-requisition.html'
    context = {
        'form':form,
        
    }
    return render(request,template,context)

def add_requisition_detail(request,pk):
    requisition= Requisition.objects.get(id=pk)
    detail = Requisition_Details.objects.filter(requisition_id=requisition.id)
    production = Restock_details.objects.filter(requisition=requisition.id)
    if production:
        # gross_bags_value =  production.aggregate(cc=Sum((int('quantity_produced') * float('product__unit_price'))))
        product = Products.objects.get(name='Sachet Water')
        gross_total = production.aggregate(cc=Sum('wages'))
        gross_bags = production.aggregate(cc=Sum('quantity_produced'))
        tt = gross_total['cc']
        bb = gross_bags['cc']
        vv = bb * product.unit_price
        
    else:
        tt = 0.00
        bb = 0.00
        vv=0.00
   
    
    if request.method == 'POST':
        form = RequisitionDetailForm(request.POST)
        if form.is_valid():
            cc=form.save(commit=False)
            cc.requisition_id=requisition
            cc.save()
            messages.info(request,'Item added')
            return redirect('products:add_requisition_detail' , requisition.id)
    else:
        form = RequisitionDetailForm()

    template = 'products/requisition_detail.html'
    context = {
        'form':form,
        'detail':detail,
        'requisition':requisition,
        'production':production,
        'tt':tt,
        'bb':bb,
        'vv':vv
       
        
    }
    return render(request,template,context)

def delete_requisition_item(request,pk):
    requisition= Requisition_Details.objects.get(id=pk)
    kk=requisition.requisition_id.id
    requisition.delete()
    messages.error(request,'Item Deleted')
    return redirect('products:add_requisition_detail', kk)

def cancel_requisition(request,pk):
    requisition = Requisition.objects.get(id=pk)
    # detail = Requisition_Details.objects.filter(requisition_id=details.id)
    requisition.status="Cancelled"
    requisition.save()
    messages.error(request,'Requisition Cancelled')
    return redirect('products:add_requisition_detail',requisition.id)

def approve_requisition(request,pk):
    requisition = Requisition.objects.get(id=pk)
    # detail = Requisition_Details.objects.filter(requisition_id=details.id)
    requisition.status="Approved"
    requisition.save()
    messages.error(request,'Requisition Approved Please Proceed to Issue Raw Material')
    return redirect('products:add_requisition_detail',requisition.id)

def issue_requisition(request,pk):
    requisition = Requisition.objects.get(id=pk)
    # detail = Requisition_Details.objects.filter(requisition_id=details.id)
    requisition.status="Issued"
    requisition.save()
    messages.error(request,'Raw material Issued')
    return redirect('products:add_requisition_detail',requisition.id)

def reverse_requisition(request,pk):
    requisition = Requisition.objects.get(id=pk)
    # detail = Requisition_Details.objects.filter(requisition_id=details.id)
    requisition.status="Pending"
    requisition.save()
    messages.error(request,'Requisition Cancelled')
    return redirect('products:add_requisition_detail',requisition.id)

def list_inventory(request,pk):
    details = Requisition_Details.objects.get(id=pk)
    requisition = Requisition.objects.get(id = details.requisition_id.id)
    inventory = RawMaterialInventory.objects.get(material_id = details.material_id.id )
    inventory_detail =  Inventory_Details.objects.filter(inventory_id = inventory.id,avialable_quantity__gt = 0).order_by('expiring_date')
    template = 'products/inventorylisting.html'
    context = {
      
        'inventory': inventory,
        'inventory_detail':inventory_detail,
        'details':details,
        'requisition':requisition,
        
        }
    return render(request, template, context)


def issue_quantity(request,requisition_id,detailbatch_id):
    detail = Requisition_Details.objects.get(id=requisition_id)
    item_inventory = RawMaterialInventory.objects.get(material_id = detail.material_id)
    inventory_detail =  Inventory_Details.objects.get(batch_number = detailbatch_id,inventory_id=item_inventory.id)
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            qty = form.cleaned_data['quantity_approved']
            if qty > item_inventory.avialable_quantity:
                messages.error(request, "Qantity approved cannot be more than" + " " + str(item_inventory.avialable_quantity))
                return redirect('products:issue_quantity', detail.id,inventory_detail.batch_number)
            else:
                
                if form.cleaned_data['quantity_approved'] > detail.quantity:
                    messages.error(request,"Quantiy Issued Cannot be more than quantity requested")
                    return redirect('products:issue_quantity', detail.id,inventory_detail.batch_number)
                else:
                    inventory_detail.quantity_requested += qty
                    inventory_detail.save()
                    item_inventory.avialable_quantity -= qty
                    item_inventory.save()
                    # detail.quantity_issued = qty
                    # detail.save()
                messages.success(request,"Approved Issued Quantity Entered")
                return redirect('products:list_inventory', detail.id)
    else:
        
        form = QuantityForm()
    template = 'products/quantityform.html'
    context = {
        'form': form,
        'item_inventory': item_inventory,
        
        'detail':detail,
        }
    return render(request, template, context)

