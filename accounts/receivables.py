
from django.shortcuts import render, redirect
from django.db import models
from crum import get_current_user
from django.db.models import Count
from django.conf import settings
from django.contrib.sessions.models import Session
from .forms import *
from .models import *
from django.db.models import Sum
from .filters import *
import datetime
from django.contrib import messages


def manage_receivables(request):
    payables = Revenue.objects.filter(amount__gt=0.00)
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))

    myFilter = ReceivableFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))
    template = 'accounts/receivables.html'
    context={
        'payables':payables,
        'total_payables':total_payables,
        'payable_value':payable_value,
        'myFilter':myFilter,
       
    }
    return render(request,template,context)



def receive_payment(request, pk):# to visit again

    
   
    today =datetime.date.today()
    accounts = Sub_Accounts.objects.filter(code__tag = 'Cash-Eq').order_by('sub_description')
    payables = Account_Receivables.objects.get(id=pk)
    offering = Orders.objects.get(id=payables.reference.id)
    general_ledger = General_Ledger.objects.filter(transactionref=offering.id)
    
    if request.method == "POST":
        
        ff = Accumulated_fund.objects.all().order_by('id').last()
        if ff is None :
            messages.success(request,'You cannot post an offering until you start an accounting year')
            return redirect('accounts:receive_payment',payables.id)
        elif ff.status == 'Closed':
            messages.success(request,'You cannot post an offering until you start an accounting year')
            return redirect('accounts:receive_payment',payables.id)
        
        form = paymentform(request.POST)
        code = request.POST.get("code")
        a,_= code.split('-----')
        if form.is_valid():
            amount_paid = form.cleaned_data.get("amount_paid")

            payables.amount -= amount_paid
            payables.save()
            aa = amount_paid
            
            subcode = Sub_Accounts.objects.get(sub_code = a)
            
            All_Transaction.objects.create(transaction_date=today,sub_code=subcode,description="Supply of Water",amount=amount_paid,account_period=ff)
            General_Ledger.objects.create(transaction_date=today,sub_code=subcode,description="Supply of Water",debit=amount_paid,transactionref=offering.id,account_period=ff)
            offering.offstatus = "Transact"
            offering.save()
            messages.success(request, "Sales Recoded, General Ledger Updates")
            return redirect('accounts:receive_payment',payables.id)
    else:
        form = paymentform()
    

    context = {
        
        'payables':payables,
        'accounts':accounts,
        'general_ledger':general_ledger,
        'form':form
        
    }
    template = 'accounts/rec_payment.html'
    return render(request, template, context)




