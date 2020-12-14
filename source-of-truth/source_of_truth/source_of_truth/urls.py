from django.conf.urls import include
from django.contrib import admin
from django.urls import path

from .views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_system_api.urls')),
    path('home/', home)
]
