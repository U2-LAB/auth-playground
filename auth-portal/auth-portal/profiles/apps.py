from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'profiles'

    def ready(self):
        import profiles.signals
