from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, authentication, permissions

from django.contrib.auth import get_user_model

from .serializers import AuthTokenSerializer, UserSerializer


class CreateTokenView(ObtainAuthToken):
    """
    Cria um novo token para autenticar o usuário
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ViewUsers(generics.ListAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

