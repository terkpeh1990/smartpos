
from math import prod
from unicodedata import name
from django.urls import path
from .import views
from .import category
from .import products,restock

app_name = 'products'

urlpatterns = [
 path('manage_category',category.manage_category,name='manage_category'),
 path('delete_category/<str:pk>/',category.delete_category,name='delete_category'),
 path('edit_category/<str:pk>/',category.edit_category,name='edit_category'),

 path('manage_product',products.manage_product,name='manage_product'),
 path('edit_product/<str:pk>/',products.edit_product,name='edit_product'),
 path('delete_product/<str:pk>/',products.delete_product,name='delete_product'),

 path('manage_rawmaterial',products.manage_raw,name='manage_raw'),
 path('edit_rawmaterial/<str:pk>/',products.edit_rawmaterial,name='edit_rawmaterial'),
 path('delete_rawmaterial/<str:pk>/',products.delete_rawmaterial,name='delete_rawmaterial'),

 path('manage_restock',restock.restock,name='manage_restock'),
 path('restock/new/',restock.add_restock,name='add_restock'),
 path('restock/<str:pk>/edit/',restock.edit_restock,name='edit_restock'),
 path('restock/<str:pk>/delete/',restock.delete_restock,name='delete_restock'),
 path('restock/new/<str:pk>/detail/',restock.add_restock_detail,name='add_restock_detail'),
 path('restock/edit/<str:pk>/detail/',restock.edit_restock_detail,name='edit_restock_detail'),
 path('restock/detail/<str:pk>/item/delete/',restock.delete_restock_item,name='delete_restock_item'),

 path('restock/<str:pk>/cancel/',restock.cancel_restock,name='cancel_restock'),
 path('restock/<str:pk>/approve/',restock.approve_restock,name='approve_restock'),
 path('restock/<str:pk>/reverse/',restock.reverse_restock,name='reverse_restock'),
 path('restock/<str:pk>/reverse/',restock.reverse_restock,name='reverse_restock'),

 path('raw_material/inventory/',restock.inventory,name='inventory'),
 path('raw_material/inventory/<str:pk>/detail/',restock.detail_inventory,name='detail_inventory'),

 path('requisition/',restock.requisition,name='requisition'),
 path('requisition/new/',restock.add_requisition,name='add_requisition'),
 path('requisition/<str:pk>/add_details/',restock.add_requisition_detail,name='add_requisition_detail'),
 path('requisition/item/<str:pk>/delete/',restock.delete_requisition_item,name='delete_requisition_item'),
 path('requisition/<str:pk>/cancel/',restock.cancel_requisition,name='cancel_requisition'),
 path('requisition/<str:pk>/approve/',restock.approve_requisition,name='approve_requisition'),
 path('requisition/<str:pk>/issue_requisition/',restock.issue_requisition,name='issue_requisition'),
 path('requisition/<str:pk>/reverse/',restock.reverse_requisition,name='reverse_requisition'),
 path('requisition/item/<str:pk>/listing/',restock.list_inventory,name='list_inventory'),
 path('requisition/<str:requisition_id>/<str:detailbatch_id>/approve/quantity/',restock.issue_quantity,name='issue_quantity'),



]