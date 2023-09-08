
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