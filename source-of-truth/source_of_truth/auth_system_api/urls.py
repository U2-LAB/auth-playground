from django.urls import path
from .views import Auth, Permission, GetPerson, GetAllPerson, logout_user

urlpatterns = [
    path('Auth', Auth),
    path('Permission', Permission),
    path('GetPerson', GetPerson),
    path('GetAllPerson', GetAllPerson),
    path('logout', logout_user)
]
