from urllib.parse import parse_qs, urlparse

from django.contrib.auth import authenticate, login, logout
from django.http.response import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.decorators.csrf import csrf_exempt
from phonenumber_field.phonenumber import PhoneNumber
from rest_framework.decorators import api_view
from rest_framework.response import Response


from .models import User


@api_view(['GET', 'POST'])
def auth(request):
    session_id = ''
    error_code = ''
    permission = 'READ'
    expire_date = ''
    try:
        logout(request)
    except Exception as e:
        error_code = f'Can\'t logout. Error {e}'
    else:
        try:
            user = authenticate(username=request.data['username'], password=request.data['password'])
        except MultiValueDictKeyError:
            error_code = 'Error in Key name. Must be `username` and `password`'
        else:
            if user is not None:
                login(request, user)
                session_id = request.session.session_key
                permission = 'READ'
                expire_date = request.session.get_expiry_date()
            else:
                session_id = 0
                error_code = 'Incorrect user name or password'
    return JsonResponse(
        {
            "SessionId": session_id,
            "ErrorCode": error_code,
            "Permission": permission,
            "ExpireDate": expire_date,
        }
    )


USER_FIELDS = ['Email', 'Username', 'First_Name', 'Last_Name', 'Phone', 'Skype']


@csrf_exempt
@api_view(['GET'])
def get_person(request):
    error_code = ''
    permission = 'READ'
    profile = {}
    if not request.session.is_empty():
        url = parse_qs(urlparse(request.build_absolute_uri()).query)  # parse QueryString from url
        try:
            person_id_obj = url.get('personId', None)
            if person_id_obj:
                person_id = int(person_id_obj[0])
            else:
                person_id = request.session['_auth_user_id']
        except ValueError:
            error_code = "KeyError querystring must be contain `personId`",
        else:
            try:
                user = User.objects.get(id=person_id)
            except User.DoesNotExist:
                error_code = "User does not exist"
            else:
                profile = {field: _get_value(user, field.lower()) for field in USER_FIELDS}
    else:
        error_code = "Session expired"
    return JsonResponse(
        {
            "ErrorCode": error_code,
            "Permission": permission,
            "Profile": profile,
        }
    )


def _get_value(user, field):
    value = user.__getattribute__(field)
    if field == 'phone' and isinstance(value, PhoneNumber):
        return value.raw_input
    else:
        return value


@api_view(['GET'])
def get_all_person(request):
    error_code = ''
    permission = 'READ'
    users = []
    if not request.session.is_empty():
        for user in User.objects.all():
            users.append({field: _get_value(user, field.lower()) for field in USER_FIELDS})
    else:
        error_code = "Session expired"
    return Response(
        {
            "ErrorCode": error_code,
            "Permission": permission,
            "Users": users,
        }
    )


@api_view(['GET'])
def logout_user(request):
    logout(request)
    return Response()
