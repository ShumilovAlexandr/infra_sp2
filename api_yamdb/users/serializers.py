from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    @staticmethod
    def validate_username(username):
        if username == 'me':
            error_massage = 'me не может использоваться как username'
            raise serializers.ValidationError(error_massage)
        return username


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

    @staticmethod
    def validate(data):
        username = data['username']
        confirmation_code = data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            error_massage = 'confirmation_code не прошел проверку'
            raise serializers.ValidationError(error_massage)
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        model = User

    @staticmethod
    def validate_username(username):
        if username == 'me':
            error_massage = 'me не может использоваться как username'
            raise serializers.ValidationError(error_massage)
        return username
