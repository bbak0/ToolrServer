from django.db import models
from datetime import datetime, timedelta
from django.utils import timezone
import random

def get_expire_time():
    return timezone.now() + timedelta(days=1)

def get_token():
    return random.getrandbits(256)

def get_sentinel_user():
    return UserProfile.objects.get_or_create(username='deleted')[0]

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

class Tool(models.Model):
    availability = models.BooleanField(default = True)
    category = models.PositiveSmallIntegerField(default = 0)
    description = models.TextField()
    location_lat = models.FloatField(default = 0)
    location_lon = models.FloatField(default = 0)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    owner = models.ForeignKey('UserProfile',
                                related_name='tool_owner',
                                on_delete=models.CASCADE)
    lent_to = models.ForeignKey('UserProfile',
                                related_name='tool_borrower',
                                on_delete=models.PROTECT)

class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey('UserProfile',
                                related_name='sender',
                                on_delete=models.SET(get_sentinel_user))
    recipient = models.ForeignKey('UserProfile',
                                related_name='recipient',
                                on_delete=models.SET(get_sentinel_user))

class Picture(models.Model):
    picture = models.ImageField()
    tool = models.ForeignKey('Tool', related_name='tool', on_delete=models.CASCADE)
