import random
from faker.providers.person.en import Provider
from random import shuffle, seed, choice

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from progress.bar import Bar


class Command(BaseCommand):
    help = 'Fill django_db database with User info'
    USER_COUNT = 1000
    
    def _get_phone(self):
        count_number = 7
        phone = '+37529'
        for _ in range(count_number):
            phone = "".join([phone, str(random.randint(0, 9))])
        return phone

    def handle(self, *args, **options):
        bar = Bar('Create user', max=self.USER_COUNT)
        User = get_user_model()
        first_names = list(set(Provider.first_names))[0:self.USER_COUNT]
        seed(1234124)
        shuffle(first_names)

        first_name = None
        last_name = None
        email = None
        phone = None
        skype = None
        password = None

        for first_name in first_names:
            first_name = first_name
            last_name = choice(first_names)
            email = first_name + "@mail.ru"
            phone = self._get_phone()
            skype = ".".join([first_name, last_name])
            password = first_name
            try:
                new_user = User.objects.create_user(
                    username=first_name,
                    password=password,
                    email=email,
                    phone=phone,
                    skype=skype,
                    first_name=first_name,
                    last_name=last_name,
                )
                new_user.save()
                
            except (ValueError, IntegrityError):
                print("duplicate")
            bar.next()
        bar.finish()
