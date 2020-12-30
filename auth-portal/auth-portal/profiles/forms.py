from django import forms

from .models import User


class UserForm(forms.Form):
    class Meta:
        model = User
        fields = ["username", "password"]
