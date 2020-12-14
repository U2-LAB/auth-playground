from django.contrib.auth import login, authenticate, logout
from django.forms import modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic.detail import DetailView
from oauth2_provider.models import get_application_model
from oauth2_provider.views.application import ApplicationRegistration, ApplicationUpdate

from api.services import DataService
from .forms import UserForm
from .models import User
from .services import OauthServices

oauth_service = OauthServices()
data_service = DataService()


class MyAppReg(ApplicationRegistration):
    def get_form_class(self):
        """
        Returns the form class for the application model
        """
        return modelform_factory(
            get_application_model(),
            fields=(
                "name", "client_id", "client_secret", "redirect_uris", "scope"
            )
        )

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.authorization_grant_type = 'authorization-code'
        form.instance.client_type = 'confidential'
        return super().form_valid(form)


class MyAppUpdate(ApplicationUpdate):
    def get_form_class(self):
        """
        Returns the form class for the application model
        """
        return modelform_factory(
            get_application_model(),
            fields=(
                "name", "client_id", "client_secret", "redirect_uris", "scope"
            )
        )


class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name = 'profiles/user_detail.html'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = self.get_object()
        context["apps"] = [token.application for token in user_object.oauth2_provider_accesstoken.all()]
        context["user_data"] = data_service.get_user_data(self.request)["Profile"]
        return context

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, **kwargs):
        oauth_service.revoke_token(request)
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def login_user(request):
    """Login user by session from service of truth"""
    next_url = request.GET.get('next', '')
    if request.method == "POST" and request.POST.get("logout"):
        logout(request)
        form = UserForm()

    elif request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            response = data_service.authorize_user_by_request(request).json()
            user_credentials = {
                "username": request.POST['username'],
                "password": request.POST['password']
            }
            next_url = request.POST.get('next', '')

            if not response["ErrorCode"]:
                request.session["expire_date_API"] = response["ExpireDate"]
                user = authenticate(request, **user_credentials)

                if not user:
                    user = User.objects.create_user(**user_credentials)

                user.session_id_for_data_service = response["SessionId"]
                user.save()

                login(request, user)
                return HttpResponseRedirect(next_url)

    else:
        form = UserForm()

    if not next_url:
        next_url = '/user/'

    return render(request, "profiles/login.html", {'next': next_url, 'form': form})


def go_home(request):
    return redirect(reverse('login'))
