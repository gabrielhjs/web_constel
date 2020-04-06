from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from ..models import Ont, Cliente, OntEntrada, OntSaida, OntAplicado


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer para o objetos de autenticação de usuários
    """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    username = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """
        Valida e autentica usuario
        """
        username = attrs.get('username')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=username,
            password=password
        )

        if not user:
            msg = 'Usuário não autenticado, login e/ou senha incorretos'
            raise serializers.ValidationError(msg, code='authentication')

        attrs['user'] = user

        return attrs


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', )


class SerializerOntBaixa(serializers.Serializer):

    porta = serializers.CharField()
    estado_link = serializers.CharField()
    nivel_ont = serializers.FloatField()
    nivel_olt = serializers.FloatField()
    nivel_olt_tx = serializers.FloatField()
    serial = serializers.CharField()
    modelo = serializers.CharField()
    contrato = serializers.IntegerField()
    token = serializers.CharField()

    def validate(self, attrs):
        serial = attrs.get('serial').upper()
        # modelo = attrs.get('modelo').upper()

        if not Ont.objects.filter(codigo=serial).exists():
            msg = 'Esta ONT não está cadastrada no sistema, entre em contato com o almoxarifado'
            raise serializers.ValidationError(msg)

        else:
            ont = Ont.objects.get(codigo=serial)
            entrada = OntEntrada.objects.filter(ont__codigo=serial).latest('data')
            user = Token.objects.get(key=attrs.get('token')).user

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
                msg = 'Esta ONT já está aplicada no contrato %d, '\
                      'entre em contato com o almoxarifado' % ont_cliente.contrato
                raise serializers.ValidationError(msg)

            elif ont.status == 3:
                msg = 'Esta ONT consta como defeituosa no sistema, entre em contato com o almoxarifado'
                raise serializers.ValidationError(msg)

            elif ont.status == 4:
                msg = 'Esta ONT consta como retirada no sistema e deve ser triada para que possa ser aplicada '\
                      'novamente, entre em contato com o almoxarifado'
                raise serializers.ValidationError(msg)

        return attrs

    def save(self):
        serial = self.validated_data.get('serial').upper()
        ont = Ont.objects.get(codigo=serial)
        ont_saida = OntSaida.objects.filter(ont__codigo=serial).latest('data')
        user = Token.objects.get(key=self.validated_data.get('token')).user

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
