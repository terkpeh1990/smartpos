from django.db.models.signals import post_save
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth import user_logged_in
from django.dispatch.dispatcher import receiver

from django.shortcuts import redirect
# from django.core.mail import send_mail,EmailMessage
from .import models

from django.contrib.auth import  get_user_model   

from .import views
from .models import *

User = get_user_model()

def customer_profile(sender, instance, created, **kwargs):
	if created:
        
		group = Group.objects.get(name='standard')
		instance.groups.add(group)
		print('Group created!')
post_save.connect(customer_profile, sender=User)


