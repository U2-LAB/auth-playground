from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.go_home, name="home"),
    path('login/', views.login_user, name="login"),
    path("user/", login_required(views.UserDetailView.as_view()), name='user_detail'),
    path("oauth/applications/register/", views.MyAppReg.as_view()),
    path("oauth/applications/<int:pk>/update/", views.MyAppUpdate.as_view())
]
