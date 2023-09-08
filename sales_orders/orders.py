from django.shortcuts import render, redirect
# from importlib_metadata import re
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Products
from django.db.models import Sum
from restock.models import Inventory
from accounts.models import Account_Receivables, General_Ledger, All_Transaction,Accumulated_fund, Sub_Accounts



def manage_orders(request):
    orders = Orders.objects.all()

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            stock=form.save()
            messages.success(request,'Please Select items for this order')
            return redirect('orders:add_orders',stock.id)
    
    else:
        form = OrderForm()

    template = 'orders/manage_order.html'

    context = {
        'orders': orders,
        'form':form,
    }

    return render(request,template,context)



def add_orders(request,pk):
    order = Orders.objects.get(id=pk)
    details = Order_details.objects.filter(order=order)
    if details:
        gross_total = details.aggregate(cc=Sum('gross_price'))
        tt = gross_total['cc']
        
    else:
        tt = 0.00
        

    if request.method =='POST':
        form = OrderDetailForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data.get("item")
            print(product)
            pro = Products.objects.get(name=product)
            cc = form.save(commit=False)
            cc.order = order
            cc.unit_price = pro.unit_price
            cc.save()
            messages.success(request,'Item Selected')
            return redirect('orders:add_orders', order.id)

    else:
        form = OrderDetailForm()

    template = 'orders/add_order.html'

    context = {
        'order': order,
        'details':details,
        'form':form,
        'tt':tt
    }

    return render(request,template,context)


def order_summery(request,pk):
    order = Orders.objects.get(id=pk)
    general_ledger = General_Ledger.objects.filter(transactionref=order.id)
    details = Order_details.objects.filter(order=order)
    if details:
        gross_total = details.aggregate(cc=Sum('gross_price'))
        tt = gross_total['cc']
        
    else:
        tt = 0.00
        

    template = 'orders/order_summery.html'

    context = {
        'order': order,
       
        'tt':tt,
        'details':details,
        'general_ledger':general_ledger
    }

    return render(request,template,context)

def remove_item(request,pk):
    item = Order_details.objects.get(id=pk)
    ff=item.order.id
    item.delete()
    messages.success(request,'Item Removed')
    return redirect('orders:add_orders', ff)


def approve_order(request,pk):
    item = Orders.objects.get(id=pk)
    item.status = 'approved'
    item.save()
    messages.success(request,'Order Approved , Kindly comfirm the Supply')
    return redirect('orders:order_summery', item.id)



def comfirm_order(request,pk):
    order = Orders.objects.get(id=pk)
    details = Order_details.objects.filter(order=order)
    sub_code = Sub_Accounts.objects.get(sub_description='SALES')
    ff = Accumulated_fund.objects.all().order_by('id').last()
    if ff is None :
        messages.success(request,'You cannot comfirm a supply until you start an accounting year')
        return redirect('orders:order_summery', order.id)
    elif ff.status == 'Closed':
        messages.success(request,'You cannot comfirm a supply until you start an accounting year')
        return redirect('orders:order_summery', order.id)
    else:
        if details:
            gross_total = details.aggregate(cc=Sum('gross_price'))
            tt = gross_total['cc']
            
        else:
            tt = 0.00

        for item in details:
            try:
                if Inventory.objects.filter(product = item.item).exists():
                    item_inventroy = Inventory.objects.get(product=item.item)
                    item_inventroy.outgoing += item.quantity
                    item_inventroy.save()
                else:
                    pass

            except Inventory.DoesNotExist:
                pass
        General_Ledger.objects.create(transaction_date=order.order_date,sub_code=sub_code,description="Supply of Water" ,cedit=tt,account_period=ff,transactionref=order.id)
        Account_Receivables.objects.create(transaction_date = order.order_date,sub_code=sub_code,description="Supply of Water",amount=tt,reference=order,account_period=ff)
        All_Transaction.objects.create(transaction_date=order.order_date,sub_code=sub_code,description="Supply of Water",amount=tt,account_period=ff)
    order.status = 'comfirmed'
    order.save()
    messages.success(request,'Supply Comfirmed')
    return redirect('orders:order_summery', order.id)
            


        
