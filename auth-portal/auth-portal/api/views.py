from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from oauth2_provider.models import RefreshToken
from users.models import MyApplication
from oauth2_provider.views import ProtectedResourceView
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ApplicationSerializer, UserSerializer
from users.models import User

from rest_framework.authentication import SessionAuthentication, BasicAuthentication

from users.services import request_to_refresh_access_token


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class TokenRefresh(APIView):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(TokenRefresh, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        response = request_to_refresh_access_token(request)
        return JsonResponse(response["data"], status=response["status_code"])


class ApplicationList(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = MyApplication.objects.all()
    serializer_class = ApplicationSerializer


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request):
        user = User.objects.create_user(username=request.POST['username'], password=request.POST['password'])
        user.save()
        data = {field: user.serializable_value(field) for field in UserSerializer.Meta.fields}
        return Response(data)


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user_obj = self.get_object()
        requested_user = request.user
        if requested_user.is_staff or user_obj == requested_user:
        # if user_obj == requested_user: # TODO delete after tests
            return self.retrieve(request, *args, **kwargs)
        error_message = {"Error": "You don't have enough permissions"}
        return Response(error_message, status=403)
