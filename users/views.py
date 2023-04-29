from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from . import permissions
from .utils import decode_jwt_token
from rest_framework import exceptions
from .utils import send_email
from .utils import generate_verify_code


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        verify_code = generate_verify_code()
        send_email(email, verify_code)
        serializer.save()

        return Response(data=serializer.data)


class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first()
        if user is None:
            raise exceptions.AuthenticationFailed('User not Found')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('Incorrect password')
        token = decode_jwt_token(user)
        response = Response()
        response.data = {
            "jwt": token,
        }
        response.set_cookie(key='jwt', value=token, httponly=True) # Токен добавляем в сookie
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            "message": "success"
        }
        return response

    def delete(self, request):
        return Response(data='You can delete')


# Тестовая вьюшка
class AllUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print(request.user)
        return Response(data='ok')

