from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from rest_framework.settings import api_settings
from rest_framework import generics, authentication, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import AuthTokenSerializer, UserSerializer, SerializerOntBaixa


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


class ViewOntBaixa(generics.GenericAPIView):
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = SerializerOntBaixa
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


@api_view(['POST'])
def view_ont_baixa(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        serializer = SerializerOntBaixa(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
