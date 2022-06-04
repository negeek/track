from calendar import c
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView, RegisterView

from dj_rest_auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from rest_framework.response import Response

from rest_framework import status

from django.conf import settings
from django.utils import timezone


class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "https://trackfi.herokuapp.com/accounts/google/login/callback/"


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
