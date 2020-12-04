from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import login_user, get_access_token, UserDetailView, redirect_to_oauth_form, MyAppReg, MyAppUpdate

urlpatterns = [
    path('login/', login_user, name="login"),
    path('api/v1/noexist/callback/', get_access_token, name='token'),
    path("user/", login_required(UserDetailView.as_view()), name='user_detail'),
    path("authorize/<slug:client_id>", redirect_to_oauth_form, name="oauth_authorize"),
    path("oauth/applications/register/", MyAppReg.as_view()),
    path("oauth/applications/<int:pk>/update/", MyAppUpdate.as_view())
]
