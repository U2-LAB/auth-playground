from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend


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
    user = authenticate(username=request.data['username'], password=request.data['password'])
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

