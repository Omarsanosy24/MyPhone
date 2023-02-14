from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.core.lib import serializers
from apps.core.lib import views
from apps.core.lib.with_history import with_history

User = get_user_model()


def index(request):
    return render(request, "documentation.html")


@api_view(["GET"])
def smoke(request):
    return Response({"smoke": True})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def private_smoke(request):
    return Response({"smoke": True})


@api_view(["GET"])
def current_user(request):
    if not (user := request.user).is_authenticated:
        return Response({})
    serializer = UserSerializer(user, context={"request": request})
    return Response({"data": serializer.data})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["url", "username", "email", "is_staff"]


@with_history()
class UserViewSet(views.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
