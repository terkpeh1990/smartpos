
from math import prod
from unicodedata import name
from django.urls import path
from .import views
from .import stocking
from .import inventory
from .import damages


app_name = 'production'

urlpatterns = [
 path('manage_restock',stocking.manage_restock,name='manage_restock'),
 path('add_stock/<str:pk>/',stocking.add_stock,name='add_stock'),
 path('edit_restock/<str:pk>/',stocking.edit_restock,name='edit_restock'),
 path('delete_restock/<str:pk>/',stocking.delete_restock,name='delete_restock'),
 path('manage_inventroy',inventory.manage_inventroy,name='manage_inventroy'),
 path('item_production_history/<str:pk>/',stocking.item_production_history,name='item_production_history'),
 path('edit_item_production_history/<str:pk>/',stocking.edit_item_production_history,name='edit_item_production_history'),
 path('manage_damages',damages.manage_damages,name='manage_damages'),
 path('comfirm_damages/<str:pk>/',damages.comfirm_damages,name='comfirm_damages'),


 
]