from django.contrib.auth.models import Group
from oauth2_provider.models import AccessToken
from users.models import MyApplication
from users.models import User
from rest_framework import serializers


class ApplicationSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()

    class Meta:
        model = MyApplication
        fields = (
            "id",
            "name",
            "owner",
            "client_id",
            "client_secret",
            "redirect_uris",
            "client_type",
            "authorization_grant_type",
        )

    def get_owner(self, obj):
        data = {
            "username": obj.user.username,
            "id": obj.user.id
        }
        return data

    def get_field_names(self, *args, **kwargs):
        field_names = super(ApplicationSerializer, self).get_field_names(*args, **kwargs)
        return field_names


class AccessTokenSerializer(serializers.ModelSerializer):
    application_name = serializers.SerializerMethodField()
    application_id = serializers.SerializerMethodField()


    def get_application_name(self, token):
        return token.application.name

    def get_application_id(self, token):
        return token.application.id

    class Meta:
        model = AccessToken
        fields = (
            'token',
            'application_id',
            'application_name',
        )


class UserSerializer(serializers.ModelSerializer):
    oauth2_provider_accesstoken = AccessTokenSerializer(many=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            "first_name",
            "last_name",
            "oauth2_provider_accesstoken",
        )
