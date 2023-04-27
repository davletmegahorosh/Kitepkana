from rest_framework.response import Response
from .serializers import UsersSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status


class AuthorizationApiView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data.get('username'),
            password=serializer.validated_data.get('password')
        )

        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response(data={'your key': token.key}, status=status.HTTP_200_OK)
        return Response(data='Нам не удалось найти вашу учетную запись. '
                             'Повторите попытку или создайте новый аккаунт.',
                        status=status.HTTP_401_UNAUTHORIZED)


class RegistrationApiView(APIView):
    def post(self, request):
        serializer = UsersSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        User.objects.create_user(username=serializer.validated_data.get('username'),
                                 password=serializer.validated_data.get('password'),
                                 is_active=False)
        return Response(status=status.HTTP_201_CREATED,
                        data='Новый пользователь создан успешно!')
