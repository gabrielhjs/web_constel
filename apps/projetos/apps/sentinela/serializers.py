from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings

from .models import SentinelaContratos


class SerializerWfmContratos(serializers.Serializer):
    wfm_id = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('token') != settings.CONTWE2_TOKEN:
            msg = 'Token inválido'
            raise serializers.ValidationError({'token': [msg]})

        return attrs

    def save(self):

        if SentinelaContratos.objects.filter(wfm_id=self.validated_data.get("wfm_id")).exists():
            return True

        return False

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
    
    
class SerializerWfmNovoContrato(serializers.Serializer):
    wfm_id = serializers.IntegerField()
    sistema_ext_id = serializers.CharField(max_length=20)
    contrato = serializers.CharField(max_length=15)
    recurso = serializers.CharField(max_length=255)
    tipo = serializers.CharField(max_length=20)
    status = serializers.CharField(max_length=20)
    cidade = serializers.CharField(max_length=50)
    porta = serializers.CharField(max_length=50)
    porta_n = serializers.CharField(max_length=10)
    token = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('token') != settings.CONTWE2_TOKEN:
            msg = 'Token inválido'
            raise serializers.ValidationError({'token': [msg]})

        return attrs

    def save(self):

        contrato, created = SentinelaContratos.objects.get_or_create(
            wfm_id=self.validated_data.get("wfm_id"),
            sistema_ext_id=self.validated_data.get("sistema_ext_id"),
            contrato=self.validated_data.get("contrato"),
            recurso=self.validated_data.get("recurso"),
            tipo=self.validated_data.get("tipo"),
            status=self.validated_data.get("status"),
            cidade=self.validated_data.get("cidade"),
            porta=self.validated_data.get("porta"),
            porta_n=self.validated_data.get("porta_n"),
        )

        if created:
            return True
      
        return False

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
