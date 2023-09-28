
from unicodedata import name
from django.urls import path
from .import orders,sales_return


app_name = 'orders'

urlpatterns = [
 path('manage_orders',orders.manage_orders,name='manage_orders'),
 path('add_orders/<str:pk>/',orders.add_orders,name='add_orders'),
 path('approve_order/<str:pk>/',orders.approve_order,name='approve_order'),
 path('comfirm_order/<str:pk>/',orders.comfirm_order,name='comfirm_order'),
 path('order_summery/<str:pk>/',orders.order_summery,name='order_summery'),
 path('remove_item/<str:pk>/',orders.remove_item,name='remove_item'),

 path('creat_returns/<str:pk>/',sales_return.creat_returns,name='creat_returns'),
 path('add_return_sales/<str:pk>/',sales_return.add_return_sales,name='add_return_sales'),
 path('remove_return_item/<str:pk>/',sales_return.remove_return_item,name='remove_return_item'),
 path('manage_returns/',sales_return.manage_returns,name='manage_returns'),
 path('approve_return/<str:pk>/',sales_return.approve_return,name='approve_return'),
 path('comfirm_return/<str:pk>/',sales_return.comfirm_return,name='comfirm_return'),
 path('return_summery/<str:pk>/',sales_return.return_summery,name='return_summery'),
 path('add_return_saless/<str:pk>/',orders.add_return_saless,name='add_return_saless'),
 path('close_shitf_sales/<str:pk>/',orders.close_shitf_sales,name='close_shitf_sales'),
 path('add_sales_amount/<str:pk>/',orders.add_sales_amount,name='add_sales_amount'),

 ]
