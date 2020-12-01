from django.contrib.auth.models import AbstractUser
from multiselectfield import MultiSelectField
from oauth2_provider.models import AbstractApplication


class User(AbstractUser):
    pass


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
