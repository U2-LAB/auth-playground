from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from .views import Auth

urlpatterns = [
    path('Auth/',Auth)
]
