from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


@extend_schema_view(
    get=extend_schema(
        summary='Метод для получения детальной информации о профиле пользователя',
    ),
    put=extend_schema(
        summary='Метод для изменения профиля пользователя',
    ),
    patch=extend_schema(
        summary='Метод для частичного изменения профиля пользователя',
    ))
class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Вьюшка для того чтобы пользователь мог получать свои данные, а также
    изменять их
    """
    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'


@extend_schema_view(
    delete=extend_schema(
        summary='Метод для удаления профиля пользователя',
    ))
class ProfileDeleteView(APIView):
    """
    Вьюшка для удаления профиля пользователя
    """

    # authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user = request.user
        user.delete()
        return Response(status=204)
