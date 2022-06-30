"""track URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static  # new
from django.conf import settings  # new
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi  # new
from rest_framework import permissions

schema_view = get_schema_view(  # new
    openapi.Info(
        title="Track API",
        default_version="v1",
        description="API for track web-app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="danieladebowale192@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('cash.urls')),
    path('accounts/', include('allauth.urls')),
    #path('api-auth/', include('rest_framework.urls')),
    path('api/users/', include('users.urls')),
    #path('api/v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    # path('api/v1/dj-rest-auth/registration/',  # new
    # include('dj_rest_auth.registration.urls')),
    path('swagger/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui(
        'redoc', cache_timeout=0), name='schema-redoc'),
]
'''
if settings.DEBUG:  # new
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)'''
