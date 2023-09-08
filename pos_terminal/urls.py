"""pos_terminal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from auth_accounts import views


urlpatterns = [
    path('',views.login_view,name='log'),
    path('logouts', views.logout_request,name='logouts'),
    path('change_password', views.change_password,name='change_password'),
    path('manage_profiles', views.manage_profiles,name='manage_profiles'),
    path('reset_staff_password/<str:pk>/', views.reset_staff_password,name='reset_staff_password'),
    path('admin/', admin.site.urls),
    path('products/',include('product.urls',namespace='products')),
    path('production/',include('restock.urls',namespace='production')),
    path('accounts/',include('accounts.urls',namespace='accounts')),
    path('orders/',include('sales_orders.urls',namespace ='orders')),
]
