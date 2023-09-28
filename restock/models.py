from django.db import models
from product.models import Products
from auth_accounts.models import Profile
from simple_history.models import HistoricalRecords
from accounts.models import Sub_Accounts
from product.models import Requisition

# Create your models here.

class Restock(models.Model):
    sts= (
        ('Morning','Morning'),
        ('Evening','Evening'),
    )
    restock_date = models.DateField()
    shift = models.CharField(max_length=10, choices= sts, default='Morning')
    total_wages = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.restock_date)


class Restock_details(models.Model):
    restock = models.ForeignKey(Restock, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    quantity_produced =  models.IntegerField(default=1)
    requisition = models.ForeignKey(Requisition,on_delete=models.CASCADE,null=True,blank=True)
    expected_quantity =  models.IntegerField(default=20)
    outstanding =  models.IntegerField(default=20)
    wages = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    history = HistoricalRecords()
    def __str__(self):
        return self.product.name + ' ---- ' + str(self.quantity_produced)

    def save(self, *args, **kwargs):
        self.wages = self.product.wage_unit * self.quantity_produced
        super(Restock_details, self).save( *args, **kwargs)

class Restock_history(models.Model):
    restock_detail = models.ForeignKey(Restock_details, on_delete=models.CASCADE,null=True)
    reason = models.CharField(max_length=255,null=True)
    created = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()
    def __str__(self):
        return self.product.name + ' ---- ' + str(self.quantity)

   


class Inventory(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    instock = models.PositiveIntegerField(default=0)
    outgoing = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    avialable_stock = models.PositiveIntegerField(default=0)
    avialable_stock_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    history = HistoricalRecords()

    def __str__(self):
        return self.product.name + " " + str(self.avialable_stock)

    def save(self,*args, **kwargs):
        self.avialable_stock = self.instock - self.outgoing
        self.avialable_stock_cost = self.avialable_stock * self.unit_price
        super(Inventory, self).save(*args, **kwargs)


class Damages(models.Model):
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        
    )
    damage_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices= sts, default='pending')
    quantity =  models.IntegerField(default=1)
    
    history = HistoricalRecords()
    def __str__(self):
        return self.product.name + ' ---- ' + str(self.quantity)

   

