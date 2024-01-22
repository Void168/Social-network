from django.db import models
import uuid

from django.utils.timesince import timesince

from account.models import User
from page.models import Page

# Create your models here.
class Website(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='website', on_delete=models.CASCADE)
    url = models.CharField(blank=True, null=True, max_length=255)
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)

class PhoneNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='phone_number', on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, null=True, max_length=255)
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)
    
class PageWebsite(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Page, related_name='page_website', on_delete=models.CASCADE)
    url = models.CharField(blank=True, null=True, max_length=255)
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)

class PagePhoneNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(Page, related_name='page_phone_number', on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, null=True, max_length=255)
    is_private = models.BooleanField(default=False)
    only_me = models.BooleanField(default=False)