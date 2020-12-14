from django.contrib.auth.models import AbstractUser
from django.db import models
from multiselectfield import MultiSelectField
from oauth2_provider.models import AbstractApplication


class User(AbstractUser):
    session_id_for_data_service = models.CharField(max_length=150, null=True, blank=True)


class MyApplication(AbstractApplication):
    EMAIL = "0"
    USERNAME = "1"
    FIRST_NAME = "2"
    LAST_NAME = "3"
    PHONE = "4"
    SKYPE = "5"

    PERM_CHOICES = (
        (EMAIL, 'Email'),
        (USERNAME, 'Username'),
        (FIRST_NAME, 'First_Name'),
        (LAST_NAME, 'Last_Name'),
        (PHONE, 'Phone'),
        (SKYPE, 'Skype'),
    )

    scope = MultiSelectField(choices=PERM_CHOICES, null=True, blank=True)
