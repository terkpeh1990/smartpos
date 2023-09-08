from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .filters import *

def manage_transfer(request):
    
    payables = Transfers.objects.all()
    sub_account = Sub_Accounts.objects.filter(code__tag='Cash-Eq')
    cash_eq = sub_account.values('sub_description').annotate(total=Sum('all_transaction__amount')).values('sub_description','sub_code','total').exclude(total__lte=0)

    myFilter = TransferFilter(request.GET, queryset=payables)
    payables = myFilter.qs
    


    if request.method =='POST':
        form=transferform(request.POST)

        if form.is_valid():
            try:
                ff = Accumulated_fund.objects.all().order_by('id').last()
                if ff is None :
                    messages.success(request,'You cannot Record a tranfer until you start an accounting year')
                    return redirect('accounts:manage_transfer')
                elif ff.status == 'Closed':
                    messages.success(request,'You cannot Record a tranfer until you start an accounting year')
                    return redirect('accounts:manage_transfer')
                else:
                    cc=form.save(commit=False)
                    vv = Accumulated_fund.objects.all().order_by('id')
                    bb=vv.last()
                    cc.status= 'Pending'
                    cc.account_period=bb
                    cc.save()
                    messages.success(request,"Transfer Initiated")
                    return redirect('accounts:manage_transfer')
            except Accumulated_fund.DoesNotExist:
                pass

       

           
    else:
        form = transferform()

    template = 'accounts/manage_transfer.html'
    context={
        'payables':payables,
        'myFilter':myFilter,
        'form':form,
        'cash_eq':cash_eq,
    }
    return render(request,template,context)


def edit_transfer(request,pk):
    transfer = Transfers.objects.get(id=pk)


    if request.method =='POST':
        form=transferform(request.POST,instance=transfer)

        if form.is_valid():

            form.save()

            messages.success(request,"Transfer Edited")
            return redirect('accounts:manage_transfer')
    else:
        form = transferform(instance=transfer)

    template = 'accounts/edit-transfer.html'

    context={

        'form':form,
    }
    return render(request,template,context)

def cancel_tranfer(request,pk):
    pv = Transfers.objects.get(id=pk)
    pv.status = "Cancelled"
    pv.save()
    messages.success(request,'Transfer Cancelled')
    return redirect('accounts:manage_transfer')


def comfirm_tranfer(request,pk):
    pv = Transfers.objects.get(id=pk)
    debit_transaction=General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.toaccount_code,description=pv.tran_dec,debit=pv.amount,account_period=pv.account_period)
    credit_transaction=General_Ledger.objects.create(transaction_date=pv.transaction_date,sub_code=pv.fromaccount_code,description=pv.tran_dec,cedit=pv.amount,account_period=pv.account_period)
    All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.toaccount_code,description=pv.tran_dec,amount=pv.amount,account_period=pv.account_period)
    All_Transaction.objects.create(transaction_date=pv.transaction_date,sub_code=pv.fromaccount_code,description=pv.tran_dec,amount= -pv.amount,account_period=pv.account_period)
    
    pv.status = "Comfirmed"
    pv.save()
    messages.success(request,'Transfer Comfirmed')
    return redirect('accounts:manage_transfer')



