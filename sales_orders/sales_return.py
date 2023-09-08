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


def creat_returns(request,pk):
    order = Orders.objects.get(id=pk)
    sales = Sales_return.objects.create(order=order,sales_return_date=order.order_date)
    return redirect('orders:add_return_sales',sales.id)


def add_return_sales(request,pk):
    sales = Sales_return.objects.get(id=pk)
    
    details = Sales_return_details.objects.filter(sales_return=sales)
    if details:
        gross_total = details.aggregate(cc=Sum('gross_price'))
        tt = gross_total['cc']
        
    else:
        tt = 0.00
        

    if request.method =='POST':
        form = SalesReturnDetailForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data.get("item")
            print(product)
            pro = Products.objects.get(name=product)
            cc = form.save(commit=False)
            cc.sales_return = sales
            cc.unit_price = pro.unit_price
            cc.save()
            messages.success(request,'Item Selected')
            return redirect('orders:add_return_sales', sales.id)

    else:
        form = SalesReturnDetailForm()

    template = 'orders/sales_retun.html'

    context = {
        'sales': sales,
        'details':details,
        'form':form,
        'tt':tt
    }

    return render(request,template,context)


def remove_return_item(request,pk):
    item = Sales_return_details.objects.get(id=pk)
    ff=item.sales_return.id
    item.delete()
    messages.success(request,'Item Removed')
    return redirect('orders:add_return_sales', ff)



def manage_returns(request):
    orders = Sales_return.objects.all()
    template = 'orders/manage_returns.html'

    context = {
        'orders': orders,
        
    }

    return render(request,template,context)


def return_summery(request,pk):
    order = Sales_return.objects.get(id=pk)
    details = Sales_return_details.objects.filter(sales_return=order)
    if details:
        gross_total = details.aggregate(cc=Sum('gross_price'))
        tt = gross_total['cc']
        
    else:
        tt = 0.00
        

    template = 'orders/return_summery.html'

    context = {
        'order': order,
       
        'tt':tt,
        'details':details
    }

    return render(request,template,context)


def approve_return(request,pk):
    item = Sales_return.objects.get(id=pk)
    item.status = 'approved'
    item.save()
    messages.success(request,'Order Approved , Kindly comfirm the Supply')
    return redirect('orders:return_summery', item.id)


def comfirm_return(request,pk):
    order = Sales_return.objects.get(id=pk)
    details = Sales_return_details.objects.filter(sales_return=order)
    sub_code = Sub_Accounts.objects.get(sub_description='SALES')
    ff = Accumulated_fund.objects.all().order_by('id').last()
    if ff is None :
        messages.success(request,'You cannot comfirm a supply until you start an accounting year')
        return redirect('orders:return_summery', order.id)
    elif ff.status == 'Closed':
        messages.success(request,'You cannot comfirm a supply until you start an accounting year')
        return redirect('orders:return_summery', order.id)
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
                    item_inventroy.outgoing -= item.quantity
                    item_inventroy.save()
                else:
                    pass

            except Inventory.DoesNotExist:
                pass

        General_Ledger.objects.create(transaction_date=order.sales_return_date,sub_code=sub_code,description="Return of Supply of Water" ,debit=tt,account_period=ff,transactionref=order.order.id)
        All_Transaction.objects.create(transaction_date=order.sales_return_date,sub_code=sub_code,description="Return of Supply of Water",amount=-tt,account_period=ff)
        acc = Account_Receivables.objects.get(reference=order.order)
        acc.amount -=tt
        acc.save()
    order.status = 'comfirmed'
    order.save()
    messages.success(request,'Supply Comfirmed')
    return redirect('orders:return_summery', order.id)