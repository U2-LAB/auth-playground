import random

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from progress.bar import Bar


class Command(BaseCommand):
    help = 'Fill django_db database with User info'
    USER_COUNT = 1000

    def _get_phone(self):
        COUNT_NUMBER = 7
        phone = '+37529'
        for _ in range(COUNT_NUMBER):
            phone = "".join([phone, str(random.randint(0, 9))])
        return phone

    def add_arguments(self, parser):
        parser.add_argument('first_name', nargs='?', type=str)
        parser.add_argument('last_name', nargs='?', type=str)

    def handle(self, *args, **options):
        User = get_user_model()
        bar = Bar('Create user', max=self.USER_COUNT)
        with open(options['first_name'], 'r') as first_name_file, open(options['last_name'], 'r') as last_name_file:

            first_name = None
            last_name = None
            email = None
            phone = None
            skype = None
            password = None

            for _ in range(self.USER_COUNT):
                first_name = first_name_file.readline().strip()
                last_name = last_name_file.readline().strip()
                email = "".join([first_name, "@mail.ru"])
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
                except ValueError:
                    print('Duplicate username')
                bar.next()
        bar.finish()
