from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

admin.autodiscover()

urlpatterns = [
    path('authorize/<slug:client_id>', views.redirect_to_oauth_form, name="oauth_authorize"),
    path('users/', csrf_exempt(views.UserList.as_view())),
    path('user_data/', views.UserDetail.as_view()),
    path('applications/', views.ApplicationList.as_view()),
    path('token/refresh/', views.TokenRefresh.as_view()),
    path('noexist/callback/', views.get_access_token, name='token'),
]
