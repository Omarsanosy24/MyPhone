"""myphone URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from apps.core import openapi
from apps.core import views as core
from myphone import routes

urlpatterns = [
    path("", core.index),
    path("smoke", core.smoke),
    path("private-smoke", core.private_smoke),
    path("api/", include(routes.router.urls)),
    path("api/me", core.current_user),
    path("api/auth/", include("rest_framework.urls")),
    path("api/auth/token", obtain_auth_token),
    path("doc/openapi/", include(openapi.urlpatterns)),
]
