from django.http.response import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view


from django.contrib.auth import authenticate, login, logout
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from phonenumber_field.phonenumber import PhoneNumber

from urllib.parse import urlparse, parse_qs

from .models import User


@api_view(['GET', 'POST'])
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
    return JsonResponse(
        {
            "SessionId": SessionId,
            "ErrorCode": ErrorCode,
            "Permission": Permission,
            "ExpireDate": ExpireDate,
        }
    )


FIELDS = ['Email', 'Username', 'First_Name', 'Last_Name', 'Phone', 'Skype']


@csrf_exempt
@api_view(['GET'])
def GetPerson(request):
    ErrorCode = ''
    Permission = 'READ'
    Profile = {}
    if not request.session.is_empty():
        url = parse_qs(urlparse(request.build_absolute_uri()).query)  # parse QueryString from url
        try:
            personId_obj = url.get('personId', None)
            if personId_obj:
                personId = int(personId_obj[0])
            else:
                personId = request.session['_auth_user_id']
        except ValueError:
            ErrorCode = "KeyError querystring must be contain `personId`",
        else:
            try:
                user = User.objects.get(id=personId)
            except User.DoesNotExist:
                ErrorCode = "User does not exist"
            else:
                Profile = {field: _get_value(user, field.lower()) for field in FIELDS}
    else:
        ErrorCode = "Session expired"
    return JsonResponse(
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
    if not request.session.is_empty():
        for user in User.objects.all():
            Users.append({field: _get_value(user, field.lower()) for field in FIELDS})
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
