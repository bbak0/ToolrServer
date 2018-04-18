from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from rest_framework.authtoken.models import Token

import random
from datetime import datetime, timedelta
from gdstorage.storage import GoogleDriveStorage

# Define Google Drive Storage
gd_storage = GoogleDriveStorage()

def get_token():
    return None

def get_expire_time():
    return timezone.now() + timedelta(days=1)


def get_sentinel_user():
    return UserProfile.objects.get_or_create(username='deleted')[0]

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    adress = models.CharField(max_length = 500, default='')
    birthdate = models.DateField(default = '1970-01-01')
    email = models.EmailField()
    google_id = models.TextField()
    


class Tool(models.Model):
    availability = models.BooleanField(default = True)
    category = models.PositiveSmallIntegerField(default = 0)
    description = models.TextField()
    location_lat = models.FloatField(default = 0)
    location_lon = models.FloatField(default = 0)
    name = models.CharField(max_length=100)
    price = models.FloatField()
    owner = models.ForeignKey(User,
                            related_name='tool_owner',
                            on_delete=models.CASCADE)
    lent_to = models.ForeignKey(User,
                                related_name='tool_borrower',
                                on_delete=models.PROTECT,
                                null = True,
                                blank = True)

class Conversation(models.Model):
    user = models.ForeignKey(User,
                            related_name='user',
                            on_delete=models.CASCADE)
    partner = models.ForeignKey(User,
                            related_name='partner',
                            on_delete=models.CASCADE)
    partner_display = models.CharField(max_length=100)
    last_message = models.TextField()

    class Meta:
        unique_together = ("user", "partner")




class Picture(models.Model):
    picture = models.ImageField(upload_to='pic', storage=gd_storage)
    tool = models.ForeignKey('Tool', related_name='picture', on_delete=models.CASCADE)

class UserRating(models.Model):
    subject_user = models.ForeignKey(User, related_name='rated_user', on_delete=models.CASCADE)
    rating_user = models.ForeignKey(User, related_name='rating_user', on_delete=models.CASCADE)
    rating = models.IntegerField()

class Loan(models.Model):
    tool_owner = models.ForeignKey(User,
                                related_name='loan_owner',
                                on_delete=models.PROTECT,
                                null = True,
                                blank = True)
    borrowing_user =  models.ForeignKey(User,
                                related_name='loan_borrower',
                                on_delete=models.PROTECT,
                                null = True,
                                blank = True)
    tool = models.ForeignKey('Tool', related_name='loan_tool', on_delete=models.CASCADE)
    accepted = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)
    returned = models.BooleanField(default=False)
    rating_owner = models.IntegerField(default=-1)
    rating_borrower = models.IntegerField(default=-1)
    date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('tool', 'borrowing_user', 'date')

class Message(models.Model):
    message = models.TextField()
    sender = models.ForeignKey(User,
                                related_name='sender',
                                on_delete=models.SET(get_sentinel_user))
    recipient = models.ForeignKey(User,
                                related_name='recipient',
                                on_delete=models.SET(get_sentinel_user))
    sendAt = models.CharField(max_length=100, default=0)
    isProposal = models.BooleanField(default=False)
    proposal = models.ForeignKey(Loan,
                                related_name='proposal',
                                on_delete = models.CASCADE,
                                default = None)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
