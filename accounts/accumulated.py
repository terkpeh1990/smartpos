from django.shortcuts import render, redirect

from restock.models import Inventory
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from decimal import Decimal



def accounting_year(request):

    
    accounts = Accumulated_fund.objects.all()
    
    if request.method == 'POST':
        form = AccForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Account Saved')
            return redirect('accounts:accounting_year')
    
    else:
        form = AccForm()

    template = 'accounts/accounting_year.html'

    context = {
        'accounts': accounts,
        'form':form,
    }

    return render(request,template,context)


def start_accounting_year(request,pk):
    pv = Accumulated_fund.objects.get(id=pk)
    try:
        cc = Accumulated_fund.objects.all().order_by('id')
       
        if cc:
            if len(cc) == 1:

                pv.open_amount = 0.00
                pv.open_stock_value = 0.00
                
            else:
                acc = cc.reverse()[1]
                if acc.close_amount is None:
                    pv.open_amount = 0.00
                else:
                    pv.open_amount = acc.close_amount
                if acc.closing_stock_value is None:
                    pv.open_stock_value = 0.00
                else:
                    pv.open_stock_value  = acc.closing_stock_value
                
            
            
    except Accumulated_fund.DoesNotExist:
        pv.open_amount = 0.00
        pv.open_stock_value = 0.00
       
        pass
    pv.status = "Open"
    pv.save()
    messages.success(request,'Accounting Period Opened')
    return redirect('accounts:accounting_year')


# def set_accounting_year_closure(request,pk):
#     pv = Accumulated_fund.objects.get(id=pk)
    
#     pv.status = "Set To Close"
#     pv.save()
#     messages.success(request,'Accounting Period Closure Set. lick Close Account to End the Accounting Period')
#     return redirect('accounts:accounting_year')

def close_accounting_year(request,pk):
    pv = Accumulated_fund.objects.get(id=pk)
    try:
        inventory = Inventory.objects.all()
        if inventory:
            if inventory is None:
                closing_stock =  0.00
            else:
                closing_stock_value = inventory.aggregate(sv=Sum('avialable_stock_cost'))
                stock_value = closing_stock_value['sv']
        else:
            stock_value = 0.00
    except Inventory.DoesNotExist:
        stock_value = 0.00

    try:
        total_transaction = All_Transaction.objects.filter(account_period=pv.id)
        cash_eq = total_transaction.filter(sub_code__code__group='Revenue')
        exp = total_transaction.filter(sub_code__code__group='Expense')
        
    
        if cash_eq:
            if cash_eq is None:
                cash_value = 0.00
            else:
                cc = cash_eq.aggregate(cash=Sum('amount'))
                cash_value = cc['cash']
        else:
            cash_value = 0.00

       
        if exp:
            if exp is None:
                exp_value = 0.00
            else:
                dd= exp.aggregate(exp=Sum('amount'))
                exp_value = dd['exp']
        else:
            exp_value = 0.00

        print(cash_value)
       
        profit = (float(cash_value)+float(pv.open_amount)) -  float(exp_value)
       

        pv.close_amount = profit
        pv.closing_stock_value = stock_value
      
       
    except Accumulated_fund.DoesNotExist:
        pv.close_amount = 0.00
        pv.closing_stock_value = 0.00
        pass
    pv.status = "Closed"
    pv.save()
    messages.success(request,'Accounting Period Closed')
    return redirect('accounts:accounting_year')




def set_closure_date_accounting_year(request,pk):
    
    close_acc = Accumulated_fund.objects.get(id=pk)
    accounts = Accumulated_fund.objects.all()
    
    if request.method == 'POST':
        form = AccCloseForm(request.POST)
        if form.is_valid():
            closing_date = form.cleaned_data.get("closing_date")
            close_acc.closing_date = closing_date
            close_acc.status = "Set To Close"
            close_acc.save()
            messages.success(request,'Accounting Period Closure Set. lick Close Account to End the Accounting Period')
            return redirect('accounts:accounting_year')
    
    else:
        form = AccCloseForm()

    template = 'accounts/close_acc_date.html'

    context = {
        'accounts': accounts,
        'form':form,
    }

    return render(request,template,context)

