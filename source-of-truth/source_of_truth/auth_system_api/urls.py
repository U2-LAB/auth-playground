from django.urls import path
from .views import Auth, Permission, GetPerson, GetAllPerson, index

urlpatterns = [
    path('Auth', Auth),
    path('Permission', Permission),
    path('GetPerson', GetPerson),
    path('GetAllPerson', GetAllPerson),
    path('', index),
]
