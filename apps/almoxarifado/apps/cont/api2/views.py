from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.renderers import JSONRenderer


from .serializers import SerializerContrato
from ..models import OntSaida


class ViewContrato(APIView):
    renderer_classes = [JSONRenderer]

    def post(self, request):
        serializer = SerializerContrato(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            serial = serializer.validated_data['serial'].upper()
            saida_ont = OntSaida.objects.filter(ont__codigo=serial).latest('data')

            response = {
                'user_to': saida_ont.user_to.username,
                'user_to_first_name': saida_ont.user_to.first_name,
                'user_to_last_name': saida_ont.user_to.last_name,
            }
            status_code = status.HTTP_201_CREATED

        else:
            response = {serializer.errors}
            status_code = status.HTTP_400_BAD_REQUEST

        return Response(response, status=status_code)
