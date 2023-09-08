from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Q


def statement_of_accounts(request,pk):
    pv = Accumulated_fund.objects.get(id=pk)
    sub_account = Sub_Accounts.objects.filter(code__group='Revenue')
    expense_sub_account = Sub_Accounts.objects.filter(code__group='Expense',)
    cash_eq = sub_account.values('sub_description').annotate(total=Sum('all_transaction__amount',filter=Q(all_transaction__account_period=pv.id))).values('sub_description','sub_code','total').exclude(total__lte=0)
    expense_cash_eq = expense_sub_account.values('sub_description').annotate(total=Sum('all_transaction__amount',filter=Q(all_transaction__account_period=pv.id))).values('sub_description','sub_code','total').exclude(total__lte=0)

    total_transaction = All_Transaction.objects.filter(account_period=pv.id)
    
    rev_cash_eq = All_Transaction.objects.filter(sub_code__code__group='Revenue',account_period=pv.id)
    exp_cash_eq = All_Transaction.objects.filter(sub_code__code__group='Expense',account_period=pv.id)

   

    revv =  rev_cash_eq.aggregate(rev=Sum('amount'))
    
    expp =  exp_cash_eq.aggregate(exp=Sum('amount'))
    if expp['exp'] is None:
        total_exp = 0.00
    else:
        total_exp = expp['exp']
    
    if revv['rev'] is None:
        total_revenue = 0.00
    else:
        total_revenue  = revv['rev']
    
    if pv.open_amount is None:
        open_amount = 0.00
    else:
        open_amount = pv.open_amount
    sum_rev = float(total_revenue) + float(open_amount)
    balance_cd = float(sum_rev) - float(total_exp)
    
    # exp = total_transaction.filter(sub_code__code__group='Expense',type='Church')

    template = 'accounts/statement_of_account.html'

    context = {
        'cash_eq': cash_eq,
        'total_revenue':total_revenue,
        'sum_rev':sum_rev,
        'expense_cash_eq':expense_cash_eq,
        'total_exp':total_exp,
        'balance_cd':balance_cd,
        # 'exp':exp,
        'pv':pv,
      
    }

    return render(request,template,context)
