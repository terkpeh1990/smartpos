from django.contrib.auth.models import AbstractUser, User
from django.db import models
from crum import get_current_user
from django.db.models import Count
from django.conf import settings
from django.contrib.sessions.models import Session
from simple_history.models import HistoricalRecords
from product.utils import incrementor
from sales_orders.models import Orders
import requests
import sys



User = settings.AUTH_USER_MODEL


class Accounts(models.Model):
    sts= (
        
        ('Expense','Expense'),
        ('Cash-Eq','Cash-Eq'),
        ('Offerings','Offerings'),
        ('Sales','Sales'),
     
    )
    st= (
        ('Revenue','Revenue'),
        ('Expense','Expense'),
        ('Others','Others'),
       
     
    )
    code = models.CharField(max_length=300)
    description = models.CharField(max_length=300)
    tag = models.CharField(max_length=10, choices= sts , default='Expense')
    group = models.CharField(max_length=10, choices= st , default='Revenue')
    
    history = HistoricalRecords()

    def __str__(self):
        return  str(self.code)

class Sub_Accounts(models.Model):

    code = models.ForeignKey(Accounts, on_delete= models.CASCADE)
    sub_code = models.CharField(max_length=300)
    sub_description = models.CharField(max_length=300)
    
    history = HistoricalRecords()


    def __str__(self):
        return  str(self.sub_code) + '----' + self.sub_description


class Accumulated_fund(models.Model):
    sts= (
        ('Open','Open'),
        ('Set To Close','Set To Close'),
        ('Closed','Closed'),  
    )
    id = models.CharField(max_length=100, primary_key=True)
    description = models.CharField(max_length=300)
    status = models.CharField(max_length=50, choices= sts,blank=True, null=True)
    open_date = models.DateField()
    closing_date = models.DateField(blank=True, null=True)
    open_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    open_stock_value =models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    closing_stock_value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    close_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    history = HistoricalRecords()

    def __str__(self):
            return self.description


    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id =  "ACC"+ " "+str(number())
            while Accumulated_fund.objects.filter(id=self.id).exists():
                self.id = "ACC"+ " "+str(number())
        super(Accumulated_fund, self).save(*args, **kwargs)






class General_Ledger(models.Model):
    
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transactionref  = models.CharField(max_length=300, blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    debit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cedit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='glcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='glmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(General_Ledger, self).save(*args, **kwargs)


class All_Transaction(models.Model):
    
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='ATcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='ATmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(All_Transaction, self).save(*args, **kwargs)

class Payment_Vouchers(models.Model):
    sts= (
        ('pending','pending'),
        ('approved','approved'),
        ('cancelled','cancelled'),
        ('void','void'),
    )
    
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    id = models.CharField(max_length=100, primary_key=True)
    sub_account = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    status = models.CharField(max_length=10, choices= sts)
    created_date = models.DateField(auto_now_add=True)
    transaction_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.description


    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id =  "PV"+ " "+str(number())
            while Payment_Vouchers.objects.filter(id=self.id).exists():
                self.id = "PV"+ " "+str(number())
        super(Payment_Vouchers, self).save(*args, **kwargs)


class Pv_details(models.Model):
    id = models.AutoField(primary_key=True)
    payment_voucher = models.ForeignKey(Payment_Vouchers, on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    history = HistoricalRecords()
    def __str__(self):
        return self.payment_voucher.description + ' ---- ' + str(self.amount)

    def save(self, *args, **kwargs):
        self.amount = self.unit_price * self.quantity
        super(Pv_details, self).save( *args, **kwargs)


class Pv_Payment_History(models.Model):
   
    transaction_date = models.DateField(auto_now_add=True)
    reference = models.ForeignKey(Payment_Vouchers,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='hiscreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='hismodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return   str(self.amount)


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Pv_Payment_History, self).save(*args, **kwargs)

class Account_Payables(models.Model):
    
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference = models.ForeignKey(Payment_Vouchers,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='apcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='apmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Account_Payables, self).save(*args, **kwargs)





class Account_Receivables(models.Model):
 
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    sub_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    reference = models.ForeignKey(Orders,on_delete=models.CASCADE,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='arcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='armodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return self.sub_code.sub_code + " "+ self.description


    def save(self, *args, **kwargs):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.modified_by = user
        super(Account_Receivables, self).save(*args, **kwargs)



class Transfers(models.Model):
    sts= (
        ('Pending','Pending'),
        ('Comfirmed','Comfirmed'),
        ('Cancelled','Cancelled'),

    )
    
    id = models.CharField(max_length=100, primary_key=True)
    account_period = models.ForeignKey(Accumulated_fund, on_delete= models.CASCADE,blank=True, null=True)
    transaction_date = models.DateField()
    tran_dec = models.CharField(max_length=300,default ='Transfer' ,blank=True,null=True)
    status = models.CharField(max_length=10, choices= sts,default='Comfirmed')
    fromaccount_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE, related_name='froms')
    toaccount_code = models.ForeignKey(Sub_Accounts, on_delete=models.CASCADE, related_name='to')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_date = models.DateField(auto_now_add=True)
    created_by = models.ForeignKey('auth.User', related_name='Trcreatedby', on_delete=models.SET_NULL, blank=True, null=True,default=None)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('auth.User', on_delete=models.SET_NULL, related_name='trmodifiedby', blank=True, null=True,default=None)

    history = HistoricalRecords()

    def __str__(self):
        return str(self.amount)
    
    def save(self, *args, **kwargs):
        if not self.id:
            number = incrementor()
            self.id = 'TR'+ '' +str(number())
            while Transfers.objects.filter(id=self.id).exists():
                self.id = 'TR'+ '' + str(number())
        super(Transfers, self).save(*args, **kwargs)
    

