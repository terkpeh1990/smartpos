from re import template
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from restock.models import Restock
import datetime

# Get today's date


# from .filters import *

def create_pv(request):
    
    if request.method == "POST":
        form = PvForm(request.POST)
        if form.is_valid():
            try:
                ff = Accumulated_fund.objects.all().order_by('id').last()
                if ff is None :
                    messages.success(request,'You cannot Record an Pv until you start an accounting year')
                    return redirect('accounts:create_pv')
                elif ff.status == 'Closed':
                    messages.success(request,'You cannot Record an offering until you start an accounting year')
                    return redirect('accounts:create_pv')
                else:
                    cc=form.save(commit=False)
                    vv = Accumulated_fund.objects.all().order_by('id')
                    bb=vv.last()
                    cc.status = "pending"
                    cc.account_period=bb
                    cc.save()
                    return redirect('accounts:pv_detail',cc.id)

            except Accumulated_fund.DoesNotExist:
                pass
    else:
        form = PvForm()
    template = 'accounts/create_pv.html'
    context = {
        'form':form,
    }
    return render(request,template,context)


def pv_detail(request,pk):
    
    pv = Payment_Vouchers.objects.get(id=pk)
    form = Pv_detailsForm()
    detail = Pv_details.objects.filter(payment_voucher=pv.id)
    if detail:
        gross_total = detail.aggregate(cc=Sum('amount'))
        pv.amount = gross_total['cc']
        pv.save()
    else:
        gross_total = 0.00
        pv.amount = gross_total
        pv.save()
   

    if request.method =='POST':
        form = Pv_detailsForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.payment_voucher = pv 
            # tt= form.aggregate(cc=Sum('amount'))
            cc= form.save()
            # pv.amount +=cc.amount
            pv.save()
            messages.success(request, 'Pv item added')
            return redirect('accounts:pv_detail',pv.id)

    template = 'accounts/pv_details.html'
    context ={
        'pv':pv,
        'detail':detail,
        'gross_total':gross_total,
        'form':form,
    }
    return render(request, template, context)



def deletes_pvitems(request,pk):
    pro = Pv_details.objects.get(id=pk)
    pv = Payment_Vouchers.objects.get(id=pro.payment_voucher.id)
    pv.amount -=pro.amount
    pv.save()
    pro.delete()
    return redirect('accounts:pv_detail',pv.id)



def manage_pv(request):
    
    pv = Payment_Vouchers.objects.all()
    template = 'accounts/manage_pv.html'
    context={
        'pv':pv,
    }
    return render(request,template,context)

def pending_pv(request):
    
    pv = Payment_Vouchers.objects.all()
    template = 'accounts/manage_pv.html'
    context={
        'pv':pv,
    }
    return render(request,template,context)

def view_pv(request,pk):
    
    order = Payment_Vouchers.objects.get(id=pk)
    expenditure = Expenditure.objects.filter(transactionref=order.id)
    # general_ledger = General_Ledger.objects.filter(transactionref=order.id)
    # history = Pv_Payment_History.objects.filter(reference = order.id)
    detail = Pv_details.objects.filter(payment_voucher=order.id)
    template = 'accounts/view_pv.html'
    context = {
        'order': order,
        'detail': detail,
        'expenditure':expenditure
        
    }
    return render(request, template, context)


def cancelled(request,pk):
    pv = Payment_Vouchers.objects.get(id=pk)
    pv.status = "cancelled"
    pv.save()
    messages.success(request,'PV Cancelled')
    return redirect('accounts:view_pv',pv.id)



def approve(request,pk):
    pv = Payment_Vouchers.objects.get(id=pk)
    pv.status = "approved"
    Expenditure.objects.get_or_create(account_period=pv.account_period,transactionref=pv.id,transaction_date=pv.transaction_date,sub_code=pv.sub_account,description=pv.description,amount=pv.amount)
    pv.save()
    messages.success(request,'PV Approved')
    return redirect('accounts:view_pv',pv.id)



def void_pv(request,pk):
    pv = Payment_Vouchers.objects.get(id=pk)
    pv.status = "void"
    pv.save()
    expenditure = Expenditure.objects.get(transactionref=pv.id)
    expenditure.delete()
    messages.success(request,'PV Voided')
    return redirect('accounts:view_pv',pv.id)


def wages_pv(request,pk):
    restock = Restock.objects.get(id=pk)
    try:
        ff = Accumulated_fund.objects.all().order_by('id').last()
        if ff is None :
            messages.success(request,'You cannot Record an Pv until you start an accounting year')
            return redirect('production:add_stock', restock.id)
        elif ff.status == 'Closed':
            messages.success(request,'You cannot Record an offering until you start an accounting year')
            return redirect('production:add_stock', restock.id)
        else:
            today = datetime.date.today()
            vv = Accumulated_fund.objects.all().order_by('id')
            bb=vv.last()
            sub_account = Sub_Accounts.objects.get(sub_description='WAGES & SALARIES')
            pv, created=Payment_Vouchers.objects.get_or_create(account_period=bb,sub_account=sub_account,description="Payment of Daily Shift Wages",amount=restock.total_wages,status='pending',ref=restock.id)
            print(pv)
            pv.transaction_date=today
            pv.save()
            Pv_details.objects.get_or_create(payment_voucher=pv,description=pv.description,quantity=1,unit_price=pv.amount)
            
            return redirect('accounts:view_pv',pv.id)

    except Accumulated_fund.DoesNotExist:
        pass
    

