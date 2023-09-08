from django.db import models
from simple_history.models import HistoricalRecords
from crum import get_current_user
from django.conf import settings
from django.contrib.sessions.models import Session
from django.core.validators import RegexValidator
import datetime
from product.utils import incrementor


User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    
    user = models.OneToOneField(
        User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    profile_code = models.CharField(max_length=200, null=True, blank=True)
    profile_code_id = models.CharField(max_length=200, null=True, blank=True)
    is_manager =models.BooleanField(default=False)
    is_standard = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)
    history = HistoricalRecords()
   
    def __str__(self):
        return self.profile_code

    def save(self,*args, **kwargs):
        if not self.profile_code_id:
            number = incrementor()
            self.profile_code_id = str(number())
            self.profile_code=self.profile_code_id+self.name
            while Profile.objects.filter(profile_code_id=self.profile_code_id).exists():
                self.profile_code_id = str(number())
                self.profile_code=self.profile_code_id+self.name
        
        super(Profile, self).save(*args, **kwargs)