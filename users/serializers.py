
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from rest_framework import exceptions, serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from dj_rest_auth.serializers import LoginSerializer


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
    '''
    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = _('Must include "email" and "password".')
            raise exceptions.ValidationError(msg)'''

    def _validate_username(self, username, password):
        pass
