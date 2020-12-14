from django.urls import path

from .views import auth, get_all_person, get_person, logout_user

urlpatterns = [
    path('Auth', auth),
    path('GetPerson', get_person),
    path('GetAllPerson', get_all_person),
    path('logout', logout_user)
]
