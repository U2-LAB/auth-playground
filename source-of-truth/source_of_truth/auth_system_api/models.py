from django.db import models
from django.contrib.auth.models import AbstractUser

from phonenumber_field.modelfields import PhoneNumberField
from multiselectfield import MultiSelectField


class User(AbstractUser):
    EMAIL = 0
    USERNAME = 1
    FIRST_NAME = 2
    LAST_NAME = 3
    PHONE = 4
    SKYPE = 5

    PERM_CHOICES = (
        (EMAIL, 'Email'),
        (USERNAME, 'Username'),
        (FIRST_NAME, 'FirstName'),
        (LAST_NAME, 'LastName'),
        (PHONE, 'Phone'),
        (SKYPE, 'Skype'),
    )

    skype = models.CharField(max_length=100, blank=True)
    phone = PhoneNumberField(region='BY')
    allow_fields = MultiSelectField(choices=PERM_CHOICES)
