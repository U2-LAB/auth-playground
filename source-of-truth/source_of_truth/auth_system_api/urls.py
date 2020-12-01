from django.urls import path
from .views import Auth, GetPerson, GetAllPerson, logout_user

urlpatterns = [
    path('Auth', Auth),
    path('GetPerson', GetPerson),
    path('GetAllPerson', GetAllPerson),
    path('logout', logout_user)
]
