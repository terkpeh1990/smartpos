
from math import prod
from unicodedata import name
from django.urls import path
from .import views
from .import category
from .import products

app_name = 'products'

urlpatterns = [
 path('manage_category',category.manage_category,name='manage_category'),
 path('delete_category/<str:pk>/',category.delete_category,name='delete_category'),
 path('edit_category/<str:pk>/',category.edit_category,name='edit_category'),

 path('manage_product',products.manage_product,name='manage_product'),
 path('edit_product/<str:pk>/',products.edit_product,name='edit_product'),
 path('delete_product/<str:pk>/',products.delete_product,name='delete_product'),
]