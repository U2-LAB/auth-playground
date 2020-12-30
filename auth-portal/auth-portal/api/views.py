from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponseRedirect
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from profiles.models import MyApplication
from profiles.models import User
from profiles.services import OauthServices
from .serializers import ApplicationSerializer, UserSerializer, UserCreationSerializer
from .services import DataService

oauth_service = OauthServices()
data_service = DataService()


class TokenRefresh(APIView):
    """
    API request to refresh token
    needed data:
        client_id,
        refresh_token
    """
    authentication_classes = [OAuth2Authentication]

    def post(self, request):
        response = oauth_service.request_to_refresh_access_token(request)
        return JsonResponse(response["data"], status=response["status_code"])


class ApplicationList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = MyApplication.objects.all()
    serializer_class = ApplicationSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        credentials = {
            "username": request.POST["username"],
            "password": request.POST["password"]
        }
        user = UserCreationSerializer(data=credentials)

        if user.is_valid():
            user = User.objects.create_user(credentials)
            data = UserSerializer(user).data
        else:
            data = user._errors

        return Response(data)


class UserDetail(generics.RetrieveAPIView):
    authentication_classes = [OAuth2Authentication]
    permission_classes = []
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.auth.user

    def get(self, request, *args, **kwargs):
        scopes = self.request.auth.scopes
        data = data_service.get_user_data(self.request)["Profile"]
        response_data = {scope: data[scope] for scope in scopes}
        return JsonResponse(response_data)


def redirect_to_oauth_form(request, client_id):
    url = oauth_service.get_redirect_url(request, client_id)
    return HttpResponseRedirect(url)


def get_access_token(request):
    # TODO Delete this function, need only for tests
    """Returns the response with access token"""
    response_data = oauth_service.request_to_get_access_token(request)
    return JsonResponse(response_data)
