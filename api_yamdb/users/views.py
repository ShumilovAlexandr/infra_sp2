from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from api.permissions import IsAdmin
from api_yamdb.settings import SENDER_EMAIL
from .models import User
from .serializers import SignUpSerializer, TokenSerializer, UserSerializer


class SignUpViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data.get('email')
        user = User.objects.get_or_create(serializer.data)[0]
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            'Ваш код подтверждения для YamDB',
            f'Ваш код подтверждения: {confirmation_code}',
            SENDER_EMAIL,
            [email, ],
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class TokenViewSet(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data.get('username')
        user = get_object_or_404(User, username=username)
        token = str(AccessToken.for_user(user=user))
        return Response(
            {'token': token},
            status=status.HTTP_200_OK,
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'


class MyUserViewSet(APIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        user = self.request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def patch(self, request):
        user = self.request.user
        data = request.data
        serializer = self.serializer_class(user, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=user.role)
        return Response(serializer.data)
