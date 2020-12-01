from django.contrib.auth import login, authenticate
from django.forms import modelform_factory
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from oauth2_provider.models import get_application_model

from .forms import UserForm
from .models import User
from .services import request_to_get_access_token, revoke_token, get_user_data, get_redirect_url
from django.views.decorators.csrf import ensure_csrf_cookie
from oauth2_provider.views.application import ApplicationRegistration, ApplicationUpdate


class UserDetailView(DetailView):
    model = User
    context_object_name = "user"
    template_name = 'profiles/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_object = self.get_object()
        context["apps"] = [token.application for token in user_object.oauth2_provider_accesstoken.all()]
        context["user_data"] = get_user_data(self.request)["Profile"]
        return context

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, **kwargs):
        revoke_token(request, request.POST["app_pk"])
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


def login_temp(request):
    next_url = request.GET.get('next', '')

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
            if user:
                login(request, user)
                return HttpResponseRedirect(request.POST['next'])
            next_url = request.POST.get('next', '')
    else:
        form = UserForm()

    if not next_url:
        next_url = '/admin/'

    return render(request, "profiles/login.html", {'next': next_url, 'form': form})


def get_access_token(request):
    response = request_to_get_access_token(request)
    return JsonResponse(response.json())


def redirect_to_oauth_form(request, client_id):
    url = get_redirect_url(request, client_id)
    return HttpResponseRedirect(url)


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



# The protected user profile endpoint that will be called
# upon successful sign-in to populate the client app database
#
# @protected_resource(scopes=['read'])
# def profile(request):
#     return HttpResponse(json.dumps({
#         "id": request.resource_owner.id,
#         "username": request.resource_owner.username,
#         "email": request.resource_owner.email,
#         "first_name": request.resource_owner.first_name,
#         "last_name": request.resource_owner.last_name
#     }), content_type="application/json")



# http://127.0.0.1:8000/o/revoke_token/ revoking token
# curl -X POST -d "grant_type=password&username=<user_name>&password=<password>" -u"<client_id>:<client_secret>" http://localhost:8000/o/token/
# curl -X POST -d "grant_type=refresh_token&refresh_token=<your_refresh_token>&client_id=<your_client_id>&client_secret=<your_client_secret>" http://localhost:8000/o/token/
# curl -H "Authorization: Bearer <your_access_token>" -X POST -d"username=foo&password=bar" http://localhost:8000/users/ # New user
# http://127.0.0.1:8000/login/?next=/o/authorize/%3Fresponse_type%3Dcode%26client_id%3DfXqZCF3GCsSlKIrSwCVHgBNgbKyWFdOlqaajLiKE%26redirect_uri%3Dhttp%3A//127.0.0.1%3A8000/noexist/callback
# http://127.0.0.1:8000/o/authorize/?response_type=code&client_id=fXqZCF3GCsSlKIrSwCVHgBNgbKyWFdOlqaajLiKE&redirect_uri=http://127.0.0.1:8000/noexist/callback
# http://127.0.0.1:8000/o/applications/register/
# http://127.0.0.1:8000/o/applications