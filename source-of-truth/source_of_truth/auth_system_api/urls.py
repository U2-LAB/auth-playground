
from django.urls import path

from .views import Auth, Permission, GetPerson

urlpatterns = [
    path('Auth', Auth),
    path('Permission', Permission),
    path('GetPerson', GetPerson),
]
