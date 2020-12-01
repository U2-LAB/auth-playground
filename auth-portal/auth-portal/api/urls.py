from django.contrib import admin
from django.urls import path
from .views import UserList, UserDetails, ApplicationList, TokenRefresh

admin.autodiscover()


urlpatterns = [
    path('users/', UserList.as_view()),
    path('users/<pk>/', UserDetails.as_view()),
    path('applications/', ApplicationList.as_view()),
    path('token/refresh/', TokenRefresh.as_view()),
]
