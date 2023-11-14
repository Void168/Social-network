from django.db import models
import uuid

from django.utils.timesince import timesince

from account.models import User
# Create your models here.
class Website(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='website', on_delete=models.CASCADE)
    url = models.CharField(blank=True, null=True, max_length=255)

class PhoneNumber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='phone_number', on_delete=models.CASCADE)
    phone_number = models.CharField(blank=True, null=True, max_length=255)