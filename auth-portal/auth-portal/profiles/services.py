from urllib.parse import urlencode

import requests
from django.http import JsonResponse
from django.urls import reverse
from oauth2_provider.models import Grant, RefreshToken
from rest_framework import status

from .models import MyApplication


class OauthServices:
    _OAUTH_PATH = 'http://192.168.32.95:8000/oauth'

    def revoke_token(self, request, format=None):
        """
        Revokes token by access token
        param: if format equal "json" return JsonResponse
        """
        app_id = request.POST["app_pk"]
        application_object = MyApplication.objects.get(pk=app_id)

        url = f"{self._OAUTH_PATH}/revoke_token/"
        access_token = request.user.oauth2_provider_accesstoken.get(application_id=app_id).token
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": application_object.client_id,
            "client_secret": application_object.client_secret,
            "token": access_token
        }
        response = requests.post(url, headers=headers, data=data)

        if response.ok:
            request.user.oauth2_provider_refreshtoken.get(application_id=app_id).delete()

        if format == "json":
            return JsonResponse({
                **response.json(),
                "detail": "Access token was revoked"
            })

    def get_redirect_url(self, request, client_id):
        """Create url for oauth authorization"""
        try:
            app_obj = MyApplication.objects.get(client_id=client_id)
        except MyApplication.DoesNotExist:
            return reverse("login")
        scopes = ' '.join(app_obj.scope.choices[elem] for elem in app_obj.scope)

        # TODO Implement opportunity to work with many redirect_uris
        redirect_uri = app_obj.redirect_uris.split()[0]

        url_args = {
            "response_type": "code",
            "client_id": client_id,
            "scope": scopes,
            "redirect_uri": redirect_uri
        }
        return f'{self._OAUTH_PATH}/authorize/?{urlencode(url_args, safe="://")}'

    def request_to_refresh_access_token(self, request):
        client_id = request.POST.get("client_id", None)
        refresh_token = request.POST.get("refresh_token", None)
        error_message = {}

        try:
            app_obj = MyApplication.objects.get(client_id=client_id)
            refresh_token_obj = RefreshToken.objects.get(token=refresh_token, application__pk=app_obj.id)
        except MyApplication.DoesNotExist:
            error_message = {
                "detail": f"client_id isn't correct"
            }
        except RefreshToken.DoesNotExist:
            if RefreshToken.objects.filter(token=refresh_token):
                error_message = {
                    "detail": "client_id isn't correct"
                }
            else:
                error_message = {
                    "detail": "refresh_token isn't correct"
                }

        if error_message:
            error_info = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "data": error_message
            }
            return error_info

        client_secret = app_obj.client_secret
        url = f"{self._OAUTH_PATH}/token/"
        data = {
            "refresh_token": refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
        }
        response = requests.post(url, data=data)

        if response.ok:
            refresh_token_obj.delete()
            response.status_code = status.HTTP_201_CREATED

        response_info = {
            "status_code": response.status_code,
            "data": response.json()
        }
        return response_info

    def request_to_get_access_token(self, request):
        authorization_code = request.GET['code']
        application_to_authorize = Grant.objects.get(code=authorization_code).application
        client_id = application_to_authorize.client_id
        client_secret = application_to_authorize.client_secret
        redirect_uri = request.build_absolute_uri().split('/?')[0]

        url = f"{self._OAUTH_PATH}/token/"
        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": authorization_code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        }

        response = requests.post(url, headers=headers, data=data)
        return response
