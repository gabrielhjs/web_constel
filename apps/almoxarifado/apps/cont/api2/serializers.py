from rest_framework import serializers
from django.contrib.auth.models import User
from django.conf import settings

from ..models import Ont, Cliente, OntEntrada, OntSaida, OntAplicado


class SerializerContrato(serializers.Serializer):
    porta = serializers.CharField()
    estado_link = serializers.CharField()
    nivel_ont = serializers.FloatField()
    nivel_olt = serializers.FloatField()
    nivel_olt_tx = serializers.FloatField()
    serial = serializers.CharField()
    modelo = serializers.CharField()
    contrato = serializers.IntegerField()
    token = serializers.CharField()
    username = serializers.CharField()

    def validate(self, attrs):
        if attrs.get('token') != settings.CONTWE2_TOKEN:
            msg = 'Token inválido'
            raise serializers.ValidationError({'token': [msg]})

        serial = attrs.get('serial').upper()

        if serial.find('4857544', 0, 7) >= 0:
            if len(serial) != 16:
                serial = serial[0:16]

        elif serial.find('ZNTS', 0, 5) >= 0:
            if len(serial) != 12:
                serial = serial[0:12]

        if not Ont.objects.filter(codigo=serial).exists():
            msg = 'ONT não cadastrada no sistema'
            raise serializers.ValidationError({'serial': msg})

        else:
            ont = Ont.objects.get(codigo=serial)
            entrada = OntEntrada.objects.filter(ont__codigo=serial).latest('data')
            user = User.objects.get(username=attrs.get('username'))

            if ont.status == 0:

                OntSaida(
                    ont=ont,
                    user=user,
                    user_to=user,
                    entrada=entrada,
                ).save()

                ont.status = 1
                ont.save()

            elif ont.status == 2:
                ont_cliente = Cliente.objects.filter(ont=ont).latest('id')
                msg = f'ONT está aplicada no contrato {ont_cliente.contrato}'
                raise serializers.ValidationError({'serial': [msg]})

            elif ont.status == 3:
                msg = 'ONT consta como defeituosa no sistema'
                raise serializers.ValidationError({'serial': [msg]})

            elif ont.status == 4:
                msg = 'ONT consta como retirada, deve ser triada'
                raise serializers.ValidationError({'serial': [msg]})

        return attrs

    def save(self):
        serial = self.validated_data.get('serial').upper()

        if serial.find('4857544', 0, 7) >= 0:
            if len(serial) != 16:
                serial = serial[0:16]

        elif serial.find('ZNTS', 0, 5) >= 0:
            if len(serial) != 12:
                serial = serial[0:12]

        ont = Ont.objects.get(codigo=serial)
        ont_saida = OntSaida.objects.filter(ont__codigo=serial).latest('data')
        user = User.objects.get(username=self.validated_data.get('username'))

        cliente = Cliente(
            porta=self.validated_data.get('porta'),
            estado_link=self.validated_data.get('estado_link'),
            nivel_ont=self.validated_data.get('nivel_ont'),
            nivel_olt=self.validated_data.get('nivel_olt'),
            nivel_olt_tx=self.validated_data.get('nivel_olt_tx'),
            ont=ont_saida.ont,
            contrato=self.validated_data.get('contrato')
        )
        cliente.save()

        OntAplicado(
            saida=ont_saida,
            user=user,
            ont=ont_saida.ont,
            cliente=cliente,
        ).save()

        ont.status = 2
        ont.save()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
