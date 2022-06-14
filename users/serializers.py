
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework import exceptions, serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from rest_framework.response import Response
from track import settings
from django.urls import exceptions as url_exceptions
from .forms import CustomSetPasswordForm


class CustomRegisterSerializer(RegisterSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

    def validate(self, data):
        if data['password1'] == ' ':
            raise serializers.ValidationError(_("input password!."))
        return data

    def save(self, request):
        user = super().save(request)
        user.username = self.data.get('username')
        user.email = self.data.get('email')
        user.password1 = self.data.get('password1')
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def _validate_username(self, username, password):
        pass


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    set_password_form_class = CustomSetPasswordForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['new_password2']
