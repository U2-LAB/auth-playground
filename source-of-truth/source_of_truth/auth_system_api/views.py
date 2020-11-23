from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.utils.datastructures import MultiValueDictKeyError

from urllib.parse import urlparse, parse_qs

from .models import User

@api_view(['POST'])
def Auth(request):
    try:
        logout(request)
    except Exception as e:
        Response(
            {
                "SessionId": '',
                "ErrorCode": f'Can\'t logout. Error {e}',
                "Permission": 'READ',
            }
        )
    try:
        user = authenticate(username=request.data['username'], password=request.data['password'])
    except MultiValueDictKeyError as e:
        return Response(
            {
                "ErrorCode": 'Error in Key name. Must be `username` and `password`',
            }
        )
    if user is not None:
        login(request, user)

        return Response(
            {
                "SessionId": request.session.session_key,
                "ErrorCode": '',
                "Permission": 'READ',
            }
        )
    else:
        return Response(
            {
                "SessionId": '',
                "ErrorCode": 'Incorrect user name or password',
                "Permission": 'READ',
            }
        )

@api_view(['POST'])
def Permission(request):
    url = parse_qs(urlparse(request.build_absolute_uri()).query) # parse QueryString from url
    try:
        user_id = int(url['user_id'][0])
    except KeyError:
        return Response(
            {
                "ErrorCode": "KeyError querystring must be contain `user_id`",
            }
        )
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {
                "ErrorCode": "User does not exist",
            }
        )
    if user:
        try:
            allowed_fields = request.data['fields'].split(' ')
            user.allow_fields = allowed_fields
            user.save()
            return Response(
                {
                    "Success": 'Fields was changed',
                }
            )
        except (MultiValueDictKeyError, KeyError) as e:
           return Response(
            {
                "ErrorCode": 'Error in Key name. Must be `permission` and `fields`',
            }
        ) 
    else:
        return Response(
            {
                "ErrorCode": "You are not logged in",
            }
        )