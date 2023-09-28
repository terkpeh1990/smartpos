from unicodedata import name
from django.urls import path
from django.conf import settings
from .import accounts
from .import sub_accounts
from .import pv
from .import payerbles
from .import general_ledger
from .import receivables
from .import transfers
from .import accumulated
from .import reports
from .import dashboard


app_name = 'accounts'

urlpatterns = [
    path('manage_accounts',accounts.manage_accounts,name='manage_accounts'),
    path('edit_accounts/<str:pk>/',accounts.edit_accounts,name='edit_accounts'),

    path('sub_accounts/<str:pk>/',sub_accounts.sub_accounts,name='sub_accounts'),
    path('edit_sub_accounts/<str:pk>/',sub_accounts.edit_sub_accounts,name='edit_sub_accounts'),

    path('create_pv',pv.create_pv,name='create_pv'),
    path('pv_detail/<str:pk>/',pv.pv_detail,name='pv_detail'),
    path('deletes_pvitems/<str:pk>/',pv.deletes_pvitems,name='deletes_pvitems'),
    path('manage_pv',pv.manage_pv,name='manage_pv'),
    path('pending_pv',pv.pending_pv,name='pending_pv'),
    path('view_pv/<str:pk>/',pv.view_pv,name='view_pv'),
    path('cancelled/<str:pk>/',pv.cancelled,name='cancelled'),

    path('approve/<str:pk>/',pv.approve,name='approve'),

    path('manage_payables',payerbles.manage_payables,name='manage_payables'),
    path('make_payment/<str:pk>/',payerbles.make_payment,name='make_payment'),

    path('general_ledger',general_ledger.general_ledger,name='general_ledger'),

    
    path('manage_receivables',receivables.manage_receivables,name='manage_receivables'),
    path('receive_payment/<str:pk>/',receivables.receive_payment,name='receive_payment'),

    path('manage_transfer',transfers.manage_transfer,name='manage_transfer'),
    path('edit_transfer/<str:pk>/',transfers.edit_transfer,name='edit_transfer'),
    path('cancel_tranfer/<str:pk>/',transfers.cancel_tranfer,name='cancel_tranfer'),
    path('comfirm_tranfer/<str:pk>/',transfers.comfirm_tranfer,name='comfirm_tranfer'),

    path('accounting_year',accumulated.accounting_year,name='accounting_year'),
    path('start_accounting_year/<str:pk>/', accumulated.start_accounting_year,name='start_accounting_year'),
    path('set_closure_date_accounting_year/<str:pk>/',accumulated.set_closure_date_accounting_year,name='set_closure_date_accounting_year'),
    path('close_accounting_year/<str:pk>/',accumulated.close_accounting_year,name='close_accounting_year'),

    path('statement_of_accounts/<str:pk>/',reports.statement_of_accounts,name='statement_of_accounts'),
    path('dashboard',dashboard.dashboard,name='dashboard'),
    path('production/wages_pv/<str:pk>/',pv.wages_pv,name='wages_pv')


  
     
]
