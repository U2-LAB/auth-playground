import re

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from phonenumber_field.phonenumber import PhoneNumber

from datetime import datetime
from urllib.parse import urlparse, parse_qs

from .models import User


@api_view(['GET','POST'])
def Auth(request):
    SessionId = ''
    ErrorCode = ''
    Permission = 'READ'
    ExpireDate = ''
    try:
        logout(request)
    except Exception as e:
        ErrorCode = f'Can\'t logout. Error {e}'
    else:
        try:
            user = authenticate(username=request.data['username'], password=request.data['password'])
        except MultiValueDictKeyError:
            ErrorCode = 'Error in Key name. Must be `username` and `password`'
        else:
            if user is not None:
                login(request, user)
                SessionId = request.session.session_key
                Permission = 'READ'
                ExpireDate = request.session.get_expiry_date()
            else:
                SessionId = 0
                ErrorCode = 'Incorrect user name or password'
    return Response(
        {
            "SessionId": SessionId,
            "ErrorCode": ErrorCode,
            "Permission": Permission,
            "ExpireDate": ExpireDate,
        }
    )


FIELDS = ['Email', 'Username', 'FirstName', 'LastName', 'Phone', 'Skype']


@csrf_exempt
@api_view(['POST'])
@login_required(login_url='/form')
def Permission(request):
    Message = ''
    ErrorCode = ''
    sessionExpired = False
    try:
        req_session_key = re.search(r'sessionid=(.*)', request.headers['Cookie']).group(1)
    except (AttributeError, KeyError):
        req_session_key = None
    try:
        sessionExpired = Session.objects.get(session_key = req_session_key).expire_date <= datetime.now()
    except Session.DoesNotExist:
        sessionExpired = True
    if req_session_key and not sessionExpired:
        url = parse_qs(urlparse(request.build_absolute_uri()).query)  # parse QueryString from url
        try:
            userid = int(url['userid'][0])
        except KeyError:
            ErrorCode = "KeyError querystring must be contain `userid`"
        else:
            try:
                user = User.objects.get(id=userid)
            except User.DoesNotExist:
                ErrorCode = "User does not exist"
            else:
                try:
                    allowed_fields = {}
                    for field in FIELDS:
                        try:
                            allowed_fields[field] = True if request.data[field] == 'True' else False
                        except KeyError:
                            allowed_fields[field] = False

                    user.allow_fields = [index for index, value in enumerate(allowed_fields.values()) if value]
                    user.save()

                    Message = 'Fields was changed'
                except (MultiValueDictKeyError, KeyError):
                    ErrorCode = 'Error in Key name. Must be `permission` and `fields`'
    else:
        ErrorCode = "Session expired"
    return Response(
        {
            'ErrorCode': ErrorCode,
            'Message': Message,
        }
    ) 


@api_view(['GET'])
def GetPerson(request):
    ErrorCode = ''
    Permission = 'READ'
    Profile = {}
    sessionExpired = False
    try:
        req_session_key = re.search(r'sessionid=(.*)', request.headers['Cookie']).group(1)
    except (AttributeError, KeyError):
        req_session_key = None
    try:
        sessionExpired = Session.objects.get(session_key = req_session_key).expire_date <= datetime.now()
    except Session.DoesNotExist:
        sessionExpired = True
    if req_session_key and not sessionExpired:
        url = parse_qs(urlparse(request.build_absolute_uri()).query)  # parse QueryString from url
        try:
            personId = int(url['personId'][0])
        except KeyError:
            ErrorCode = "KeyError querystring must be contain `personId`",
        else:
            try:
                user = User.objects.get(id=personId)
            except User.DoesNotExist:
                ErrorCode = "User does not exist"
            else:
                Profile = {field: _get_value(user, field.lower()) for field in FIELDS if field in user.get_allow_fields_list()}
    else:
        ErrorCode = "Session expired"
    return Response(
        {
            "ErrorCode": ErrorCode,
            "Permission": Permission,
            "Profile": Profile,
        }
    )


def _get_value(user, field):
    value = user.__getattribute__(field)
    if field == 'phone' and isinstance(value, PhoneNumber):
        return value.raw_input
    else:
        return value


@api_view(['GET'])
def GetAllPerson(request):
    ErrorCode = ''
    Permission = 'READ'
    Users = []
    fields = ['id', 'first_name', 'last_name', 'username', 'email', 'skype', 'phone']
    sessionExpired = False
    try:
        req_session_key = re.search(r'sessionid=(.*)', request.headers['Cookie']).group(1)
    except (AttributeError, KeyError):
        req_session_key = None
    try:
        sessionExpired = Session.objects.get(session_key = req_session_key).expire_date <= datetime.now()
    except Session.DoesNotExist:
        sessionExpired = True
    if req_session_key and not sessionExpired:
        for user in User.objects.all():
            Users.append({field: _get_value(user, field) for field in fields})
    else:
        ErrorCode = "Session expired"
    return Response(
        {
            "ErrorCode": ErrorCode,
            "Permission": Permission,
            "Users": Users,
        }
    )

@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response()

def index(request):
    return render(request, 'index.html')
