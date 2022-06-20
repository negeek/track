
from enum import unique
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.translation import gettext_lazy as _
from allauth.account.adapter import get_adapter

from rest_framework import serializers

from rest_framework import exceptions, serializers
from dj_rest_auth.registration.serializers import RegisterSerializer

from dj_rest_auth.serializers import LoginSerializer, PasswordChangeSerializer
from rest_framework.response import Response
from track import settings
from django.urls import exceptions as url_exceptions
from .forms import CustomSetPasswordForm
from allauth.account import app_settings as allauth_settings
from allauth.utils import email_address_exists, get_username_max_length
from django.contrib.auth import get_user_model


def username_exists(username):
    users = get_user_model().objects
    ret = users.filter(username__iexact=username).exists()
    return ret


class CustomRegisterSerializer(RegisterSerializer):
    username = serializers.CharField(
        min_length=allauth_settings.USERNAME_MIN_LENGTH,
        required=False,  allow_blank=True, style={'input_type': 'username'})
    email = serializers.EmailField(
        required=False,  allow_blank=True, style={'input_type': 'email'})
    password1 = serializers.CharField(write_only=True, required=False, allow_blank=True, style={
                                      'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']

    def validate_username(self, username):
        if username:
            if username_exists(username):
                msg = {'error_message':  'username already exist'}
                raise serializers.ValidationError(msg)

            if len(username) > 50:
                msg = {'error_message':  'username too long'}
                raise serializers.ValidationError(msg)

            username = get_adapter().clean_username(username)

        else:
            msg = {'error_message':  'input username!'}
            raise serializers.ValidationError(msg)

        return username

    def validate_password1(self, password):

        if password:
            if len(password) < 8:
                msg = {
                    'error_message':  'password too short. Must be at least 8 characters!'}
                raise serializers.ValidationError(msg)

            if password.isdigit():
                msg = {
                    'error_message':  'password entirely numeric'}
                raise serializers.ValidationError(msg)

            if password.isalpha():
                msg = {
                    'error_message':  'password entirely alphabet'}
                raise serializers.ValidationError(msg)
            password = get_adapter().clean_password(password)

        else:
            msg = {'error_message':  'input password!'}
            raise serializers.ValidationError(msg)

        return password

    def validate_email(self, email):
        if email:
            email = get_adapter().clean_email(email)
            if allauth_settings.UNIQUE_EMAIL:
                if email and email_address_exists(email):
                    msg = {'error_message':  'Email already exist'}
                    raise serializers.ValidationError(msg)
        else:
            msg = {'error_message':  'input email!'}
            raise serializers.ValidationError(msg)

        return email

    def validate(self, data):
        return data

    def save(self, request):
        user = super().save(request)
        user.username = self.data.get('username')
        user.email = self.data.get('email')
        user.password1 = self.data.get('password1')
        user.save()
        return user


class CustomLoginSerializer(LoginSerializer):
    password = serializers.CharField(required=False, allow_blank=True, style={
        'input_type': 'password'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['username']

    def _validate_username(self, username, password):
        pass

    def _validate_email(self, email, password):
        if email and password:
            user = self.authenticate(email=email, password=password)
        else:
            msg = {'error': {'message': 'must include email and password'}}
            raise exceptions.ValidationError(msg)
            # return response

        return user

    def get_auth_user(self, username, email, password):
        """
        Retrieve the auth user from given POST payload by using
        either `allauth` auth scheme or bare Django auth scheme.
        Returns the authenticated user instance if credentials are correct,
        else `None` will be returned
        """
        if 'allauth' in settings.INSTALLED_APPS:

            # When `is_active` of a user is set to False, allauth tries to return template html
            # which does not exist. This is the solution for it. See issue #264.
            try:
                return self.get_auth_user_using_allauth(username, email, password)
            except url_exceptions.NoReverseMatch:
                msg = {
                    'error': {'message': 'Unable to log in with provided credentials.'}}
                raise exceptions.ValidationError(msg)
        return self.get_auth_user_using_orm(username, email, password)

    @ staticmethod
    def validate_email_verification_status(user):
        from allauth.account import app_settings
        if (app_settings.EMAIL_VERIFICATION == app_settings.EmailVerificationMethod.MANDATORY and not user.emailaddress_set.filter(email=user.email, verified=True).exists()):
            msg = {'error': {'message': 'E-mail is not verified.'}}

            raise serializers.ValidationError(msg)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')
        user = self.get_auth_user(username, email, password)

        if not user:
            msg = {
                'error': {'message': 'Unable to log in with provided credentials.'}}
            raise exceptions.ValidationError(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # If required, is the email verified?
        if 'dj_rest_auth.registration' in settings.INSTALLED_APPS:
            self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs


'''{
    "non_field_errors": [
        "Must include \"email\" and \"password\"."
    ]
}'''


class CustomPasswordChangeSerializer(PasswordChangeSerializer):
    set_password_form_class = CustomSetPasswordForm

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['new_password2']
