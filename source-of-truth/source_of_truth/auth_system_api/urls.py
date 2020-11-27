from django.urls import path
from .views import Auth, Permission, GetPerson, GetAllPerson, index, logout_user

urlpatterns = [
    path('Auth', Auth),
    path('Permission', Permission),
    path('GetPerson', GetPerson),
    path('GetAllPerson', GetAllPerson),
    path('', index),
    path('home',index),
    path('form',index),
    path('logout', logout_user)
]
