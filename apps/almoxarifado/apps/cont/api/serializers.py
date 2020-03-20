from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponseRedirect

from rest_framework import serializers


class AuthTokenSerializer(serializers.Serializer):
    """
    Serializer para o objetos de autenticação de usuários
    """
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
