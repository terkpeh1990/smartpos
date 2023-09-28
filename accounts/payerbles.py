from django.shortcuts import render, redirect
from .forms import *
from .models import *
from .filters import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime


def manage_payables(request):
    payables = Expenditure.objects.filter(amount__gt=0.00)
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))

    myFilter = PayablesFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    total_payables = payables.count()
    payable_value = payables.aggregate(cc=Sum('amount'))
    template = 'accounts/manage_payables.html'
    context={
        'payables':payables,
        'total_payables':total_payables,
        'payable_value':payable_value,
        'myFilter':myFilter,
    }
    return render(request,template,context)



@login_required
def make_payment(request, pk):# to visit again
    today =datetime.date.today()
    accounts = Sub_Accounts.objects.filter(code__tag='Cash-Eq').order_by('sub_description')
    payables = Account_Payables.objects.get(id=pk)
    his = Pv_Payment_History.objects.filter(reference=payables.reference.id)
    st = Payment_Vouchers.objects.get(id=payables.reference.id)
    if request.method == "POST":
        
        ff = Accumulated_fund.objects.all().order_by('id').last()
        if ff is None :
            messages.success(request,'You cannot any payment until you start an accounting year')
            return redirect('accounts:make_payment',payables.id)
        elif ff.status == 'Closed':
            messages.success(request,'You cannot make any payment until you start an accounting year')
            return redirect('accounts:make_payment',payables.id)
        else:
            form = paymentform(request.POST)
            code = request.POST.get("code")
            a,_= code.split('-----')

            if form.is_valid():
                amount_paid = form.cleaned_data.get("amount_paid")
                payables.amount -= amount_paid
                payables.save()
                cc=Pv_Payment_History.objects.create(reference=st, amount=amount_paid)
                subcode = Sub_Accounts.objects.get(sub_code = a)
                All_Transaction.objects.create(transaction_date=today,sub_code=subcode,description=st.description + " "+ " Using" + " "+ subcode.sub_description,amount=-cc.amount,account_period=ff)
                General_Ledger.objects.create(transaction_date=today,sub_code=subcode,description=st.description + " "+ " Using" + " "+ subcode.sub_description,cedit=cc.amount,transactionref=st.id,account_period=ff)
                messages.success(request, "Payment Made, General Ledger Updates")
                return redirect('accounts:make_payment',payables.id)

    else:
        form = paymentform()

    context = {
        'form': form,
        'his':his,
        'order':st,
        'payables':payables,
        'accounts':accounts,
    }
    template = 'accounts/payments.html'
    return render(request, template, context)