from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    skype = models.CharField(max_length=100, blank=True)
    phone = PhoneNumberField(region='BY')
