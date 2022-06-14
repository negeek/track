from rest_framework.permissions import AllowAny, IsAuthenticated
from typing import Tuple
from rest_framework.decorators import api_view
from calendar import c
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView, RegisterView

from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from rest_framework.response import Response

from rest_framework import status
from django.conf import settings
from django.utils import timezone
import base64
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password
from rest_framework.utils import json
from rest_framework.views import APIView
from rest_framework.response import Response
import requests
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

from django.core.exceptions import ValidationError
from rest_framework import exceptions, serializers
from .serializers import CustomPasswordChangeSerializer


def payload(id_token):
    count = 0
    indexes = []
    for i in range(len(id_token)):
        if id_token[i] == '.':
            indexes.append(i)
            count += 1
        if count >= 2:
            break
    return indexes


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': '389615847852-n6nna6ia54g6pij9l6a8vaklf467tj7j.apps.googleusercontent.com',
        'client_secret': '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',
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code',

    }

    response = requests.post('https://oauth2.googleapis.com/token', data=data)

    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')

    details = response.json()

    return details


def user_create(email, username, password=None):
    extra_fields = {
        'is_staff': False,
        'is_superuser': False,
    }

    user = User(email=email, username=username)

    if password:
        user.set_password(password)
    else:
        user.set_unusable_password()

    user.full_clean()
    user.save()

    return user


def user_get_or_create(email, username):
    user = User.objects.filter(email=email).first()

    if user:
        return user

    return user_create(email=email, username=username)


@api_view(['GET', 'POST'])
def GoogleLoginApi(request):

    code = request.GET['code']

    redirect_uri = 'http://127.0.0.1:8000/api/users/social/google/'

    tokens = google_get_access_token(
        code=code, redirect_uri=redirect_uri)

    access_token, refresh_token = tokens['access_token'], tokens['refresh_token']
    id_token = tokens['id_token']
    payloadIdx = payload(id_token)
    payloadStr = id_token[payloadIdx[0]+1:payloadIdx[1]]
    print(payloadStr)

    user_info = base64.urlsafe_b64decode(payloadStr + '===')
    user_info = json.loads(user_info.decode("utf-8"))
    # return Response(user_info)

    profile_data = {
        'email': user_info['email'],
        'username': user_info['given_name']
    }

    # We use get-or-create logic here for the sake of the example.
    # We don't have a sign-up flow.
    user = user_get_or_create(profile_data['email'], profile_data['username'])
    if user:
        success = True
    else:
        success = False

    response = {}
    response['user'] = profile_data
    response['success'] = success
    response['access_token'] = access_token
    response['refresh_token'] = refresh_token
    return Response(response)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://127.0.0.1:8000/api/users/social/google/"
    client_class = OAuth2Client


class CustomRegisterView(RegisterView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            data['success'] = True
            data['message'] = 'successfully registered'
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,


            )
        else:
            data = {}
            data['success'] = False
            data['message'] = 'Registration Failed'
            response = Response(data,
                                status=status.HTTP_204_NO_CONTENT, headers=headers,)

        return response


class CustomLoginView(LoginView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_response(self):
        serializer_class = self.get_response_serializer()

        if getattr(settings, 'REST_USE_JWT', False):
            from rest_framework_simplejwt.settings import (
                api_settings as jwt_settings,
            )
            access_token_expiration = (
                timezone.now() + jwt_settings.ACCESS_TOKEN_LIFETIME)
            refresh_token_expiration = (
                timezone.now() + jwt_settings.REFRESH_TOKEN_LIFETIME)
            return_expiration_times = getattr(
                settings, 'JWT_AUTH_RETURN_EXPIRATION', False)
            auth_httponly = getattr(settings, 'JWT_AUTH_HTTPONLY', False)

            data = {
                'user': self.user,
                'access_token': self.access_token,
            }

            if not auth_httponly:
                data['refresh_token'] = self.refresh_token
            else:
                # Wasnt sure if the serializer needed this
                data['refresh_token'] = ""

            if return_expiration_times:
                data['access_token_expiration'] = access_token_expiration
                data['refresh_token_expiration'] = refresh_token_expiration

            serializer = serializer_class(
                instance=data,
                context=self.get_serializer_context(),
            )
        elif self.token:
            serializer = serializer_class(
                instance=self.token,
                context=self.get_serializer_context(),
            )
        else:
            data = {}
            data['success'] = False
            data['message'] = 'error'
            return Response(data, status=status.HTTP_204_NO_CONTENT)

        data = {}
        data['data'] = serializer.data
        data['success'] = True
        data['message'] = 'successfully logged in'

        response = Response(data, status=status.HTTP_200_OK)

        return response


class CustomPasswordChangeView(PasswordChangeView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = CustomPasswordChangeSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'New password has been saved.',
                         'success': True})
