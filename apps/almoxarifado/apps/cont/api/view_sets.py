from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework import generics, authentication, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from .serializers import AuthTokenSerializer, UserSerializer, SerializerOntBaixa
from ..models import OntSaida


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


@api_view(['POST', ])
def view_ont_baixa(request):
    """
    List all code snippets, or create a new snippet.
    """
    if request.method == 'POST':
        serializer = SerializerOntBaixa(data=request.data)
        if serializer.is_valid():
            serializer.save()

            serial = serializer.validated_data.get('serial').upper()
            saida_ont = OntSaida.objects.filter(ont__codigo=serial).latest('data')

            response = {
                'user_to': saida_ont.user_to.username,
                'user_to_first_name': saida_ont.user_to.first_name,
                'user_to_last_name': saida_ont.user_to.last_name,
            }

            return Response(response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
