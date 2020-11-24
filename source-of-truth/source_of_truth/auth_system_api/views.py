from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.models import AnonymousUser
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
@api_view(['POST'])
def Permission(request):
    if request.session.is_empty():
        return Response(
            {
                "ErrorCode": "You are not authorized",
            }
        )
    fields = ['Email', 'Username', 'FirstName', 'LastName', 'Phone', 'Skype']
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
    try:
        allowed_fields = {}
        for field in fields:
            try:
                allowed_fields[field] = True if request.data[field]=='True' else False
            except KeyError:
                allowed_fields[field] = False
        
        user.allow_fields = [index for index, value in enumerate(allowed_fields.values()) if value]
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
