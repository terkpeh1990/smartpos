from django.shortcuts import render, redirect
import restock
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Products
from restock.models import Damages
from accounts.models import Accumulated_fund,General_Ledger, All_Transaction,Accumulated_fund, Sub_Accounts


def manage_damages(request):
    damages = Damages.objects.all()
   
    if request.method =='POST':
        form = DamageForm(request.POST)
        if form.is_valid():
           
            cc = form.save()
           
            messages.success(request,'Damage Recorded')
            return redirect('production:manage_damages')

    else:
        form = DamageForm()

    template = 'restock/damages.html'

    context = {
        'damages': damages,
        'form': form,
        
    }

    return render(request,template,context)



def comfirm_damages(request,pk):
    damage = Damages.objects.get(id=pk)
    tt = damage.product.unit_price * damage.quantity
    code = Sub_Accounts.objects.get(sub_description="CASH")
    
    ff = Accumulated_fund.objects.all().order_by('id').last()
    if ff is None :
        messages.success(request,'You cannot comfirm a supply until you start an accounting year')
        return redirect('production:manage_damages')
    elif ff.status == 'Closed':
        messages.success(request,'You cannot comfirm a supply until you start an accounting year')
        return redirect('production:manage_damages')
    else:
        try:
            if Inventory.objects.filter(product = damage.product).exists():
                item_inventroy = Inventory.objects.get(product=damage.product)
                item_inventroy.outgoing += damage.quantity
                item_inventroy.save()
            else:
                pass

        except Inventory.DoesNotExist:
            pass
        General_Ledger.objects.create(transaction_date=damage.damage_date,sub_code=damage.sub_code,description="Damage of Product" ,debit=tt,account_period=ff)
        All_Transaction.objects.create(transaction_date=damage.damage_date,sub_code=damage.sub_code,description="Damage of Product",amount=tt,account_period=ff)

    damage.status = 'approved'
    damage.save()
    messages.success(request,'Damages Comfirmed')
    return redirect('production:manage_damages')


