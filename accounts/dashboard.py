from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum,Q

from django.db.models.functions import TruncMonth
import datetime


def dashboard(request):
    today =datetime.date.today()
   
    all_orders = Orders.objects.all()
    payables = Expenditure.objects.filter(amount__gt=0.00)
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))

    rec = Revenue.objects.filter(amount__gt=0.00)
    total_rec  = rec.count()
    rec_value = rec.aggregate(cc=Sum('amount'))
    
    sub_account = Sub_Accounts.objects.filter(code__tag='Cash-Eq')
    cash_eq = sub_account.values('sub_description').annotate(total=Sum('all_transaction__amount')).values('sub_description','sub_code','total').exclude(total__lte=0)
    transfer = Transfers.objects.all()

    all_transaction = All_Transaction.objects.all().annotate(month = TruncMonth('transaction_date'))
    monthly_transaction_in_year = all_transaction.values('month').annotate(revenue=Sum('amount',filter=Q(sub_code__code__group='Revenue')),expenditure=Sum('amount',filter=Q(sub_code__code__group='Expense'))).values('month','revenue','expenditure').filter(transaction_date__year=today.year)
    
    ff = Accumulated_fund.objects.all().order_by('id').last()
    accounting_year = Accumulated_fund.objects.filter(status = 'Closed')
    if ff is None :
       open_balace = 0.00
    else:
        open_balace = ff.open_amount

  
    template = 'accounts/dashboard.html'

    context = {
        'cash_eq': cash_eq,
        'transfer':transfer,
        'all_orders':all_orders,
        'monthly_transaction_in_year':monthly_transaction_in_year,
        'open_balace':open_balace,
        'accounting_year':accounting_year,
        'payables':payables,
        'payable_value':payable_value,
        'rec_value':rec_value,
        'rec':rec
    }

    return render(request,template,context)