from django.db import models
from product.models import Products
from auth_accounts.models import Profile
from simple_history.models import HistoricalRecords
from product.utils import incrementor
from product.models import Requisition


# Create your models here.

class Orders(models.Model):
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('comfirmed','comfirmed'),
        ('posted','posted'),
    )
    id = models.CharField(max_length=100, primary_key=True)
    order_date = models.DateField()
    status = models.CharField(max_length=10, choices= sts, default='pending')
    sales_posted = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.order_date)

    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id =  "SP"+ " "+str(number())
            while Orders.objects.filter(id=self.id).exists():
                self.id = "SP"+ " "+str(number())
        super(Orders, self).save(*args, **kwargs)


class Order_details(models.Model):
   
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    item = models.ForeignKey(Products,on_delete=models.CASCADE)
    
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    quantity_returned = models.PositiveIntegerField(default=0)
    atual_quantity = models.PositiveIntegerField(default=0)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.order.id)


    def save(self,*args, **kwargs):
        self.atual_quantity = self.quantity - self.quantity_returned
        self.gross_price = self.unit_price * self.atual_quantity

        super(Order_details, self).save(*args, **kwargs)

class Sales_return(models.Model):

    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('comfirmed','comfirmed'),
    )
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    sales_return_date = models.DateField()
    status = models.CharField(max_length=10, choices= sts, default='pending')
    created = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return str(self.sales_return_date)


class Sales_return_details(models.Model):
       
    sales_return = models.ForeignKey(Sales_return, on_delete=models.CASCADE)
    item = models.ForeignKey(Products,on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    gross_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.order.id)


    def save(self,*args, **kwargs):
        self.gross_price = self.unit_price * self.quantity
        super(Sales_return_details, self).save(*args, **kwargs)
