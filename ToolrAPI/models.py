from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import random

def get_expire_time():
    return timezone.now() + timedelta(days=1)

def get_token():
    return random.getrandbits(256)

# Create your models here.
class UserProfile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    google_id = models.TextField(primary_key = True)

class AuthToken(models.Model):
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE)
    expire = models.DateTimeField(default=get_expire_time)
    token = models.TextField(default=get_token)
