
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.sessions.models import Session
import datetime
from crum import get_current_user
from .utils import incrementor
from simple_history.models import HistoricalRecords
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    history = HistoricalRecords()

    def __str__(self):
        return self.name


class Products(models.Model):
  
    id = models.CharField(max_length=2000, primary_key=True)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wage_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    

    history = HistoricalRecords()


    def __str__(self):
        return self.name


    def save(self):

        if not self.id:
            number = incrementor()
            self.id = number()
            while Products.objects.filter(id=self.id).exists():
                self.id = number()
        super(Products, self).save()


class RawMaterial(models.Model):
    name = models.CharField(max_length=250)
    unit = models.DecimalField(max_digits=10, decimal_places=2)
    history = HistoricalRecords()


    def __str__(self):
        return self.name


class RawMaterialInventory(models.Model):
    material_id =models.ForeignKey(RawMaterial,related_name ='rawmaterialinventory' ,on_delete=models.CASCADE,null=True, blank=True)
    avialable_quantity = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return str(self.id)

class Inventory_Details(models.Model):
    inventory_id =models.ForeignKey(RawMaterialInventory,related_name ='inventory_details', on_delete=models.CASCADE,null=True, blank=True)
    quantity_intake = models.PositiveIntegerField(default=0)
    quantity_requested = models.PositiveIntegerField(default=0)
    avialable_quantity = models.PositiveIntegerField(default=0)
    batch_number =  models.CharField(max_length=250)
    date_received = models.DateField(auto_now_add=True)
    expiring_date =models.DateField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['expiring_date']

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        self.avialable_quantity = self.quantity_intake - self.quantity_requested
        super(Inventory_Details, self).save(*args, **kwargs)


class Restocks(models.Model):
    
    status = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Cancelled', 'Cancelled'),
    )
    restock_date =  models.DateTimeField()
    status = models.CharField(
        max_length=10, choices=status, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    
    def __str__(self):
        return str(self.id)

       

class Restock_details(models.Model):
    restock_id =models.ForeignKey(Restocks, blank=True, related_name = 'details',on_delete=models.CASCADE,null=True)
    material_id =models.ForeignKey(RawMaterial ,on_delete=models.CASCADE,null=True, blank=True)
    quantity = models.PositiveIntegerField(default=0)
    batch_number = models.CharField(max_length=255,null=True)

    def __str__(self):
        return self.material_id.name

    def save(self, *args, **kwargs):
        if not self.batch_number:
            number = incrementor()
            self.batch_number = number()
            while Restock_details.objects.filter(batch_number=self.batch_number).exists():
                self.batch_number = number()
        super(Restock_details, self).save(*args, **kwargs)


class Requisition(models.Model):
    
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Issued', 'Issued'),
        ('Cancelled','Cancelled'),
    )
    id = models.CharField(max_length=2000, primary_key=True)
    requisition_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=stat, default="Pending", null=True, blank=True)
    
    history = HistoricalRecords()

    def __str__(self):
        return self.id

    

    def save(self, *args, **kwargs):
       
        if not self.id:
            number = incrementor()
            self.id = number()
            while Requisition.objects.filter(id=self.id).exists():
                self.id = number()
        super(Requisition, self).save( *args, **kwargs)


class Requisition_Details(models.Model):
    stat = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        
    )
    detail_date = models.DateField(auto_now_add=True,null=True, blank=True)
    material_id = models.ForeignKey(RawMaterial, on_delete= models.CASCADE,null=True, blank=True)
    quantity = models.IntegerField(default=1)
    quantity_approved = models.IntegerField(default=1)
    requisition_id = models.ForeignKey(Requisition, on_delete=models.CASCADE)

    history = HistoricalRecords()
    def __str__(self):
        return self.product.name

    

    