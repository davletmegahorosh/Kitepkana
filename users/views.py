from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from djoser import signals
from djoser.compat import get_user_email
from djoser.conf import settings
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics, permissions, status
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
import users.serializers
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from djoser.views import UserViewSet
from users.email import ActivationEmail, ConfirmationEmail
User = get_user_model()
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


class CustomDjoserViewSet(UserViewSet):
    serializer_class = settings.SERIALIZERS.user
    queryset = User.objects.all()
    permission_classes = settings.PERMISSIONS.user
    token_generator = default_token_generator
    lookup_field = settings.USER_ID_FIELD

    def permission_denied(self, request, **kwargs):
        if (
                settings.HIDE_USERS
                and request.user.is_authenticated
                and self.action in ["update", "partial_update", "list", "retrieve"]
        ):
            raise NotFound()
        super().permission_denied(request, **kwargs)

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        if settings.HIDE_USERS and self.action == "list" and not user.is_staff:
            queryset = queryset.filter(pk=user.pk)
        return queryset

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = settings.PERMISSIONS.user_create
        elif self.action == "activation":
            self.permission_classes = settings.PERMISSIONS.activation
        elif self.action == "resend_activation":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "list":
            self.permission_classes = settings.PERMISSIONS.user_list
        elif self.action == "reset_password":
            self.permission_classes = settings.PERMISSIONS.password_reset
        elif self.action == "reset_password_confirm":
            self.permission_classes = settings.PERMISSIONS.password_reset_confirm
        elif self.action == "set_password":
            self.permission_classes = settings.PERMISSIONS.set_password
        elif self.action == "set_username":
            self.permission_classes = settings.PERMISSIONS.set_username
        elif self.action == "reset_username":
            self.permission_classes = settings.PERMISSIONS.username_reset
        elif self.action == "reset_username_confirm":
            self.permission_classes = settings.PERMISSIONS.username_reset_confirm
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            self.permission_classes = settings.PERMISSIONS.user_delete
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            if settings.USER_CREATE_PASSWORD_RETYPE:
                return settings.SERIALIZERS.user_create_password_retype
            return settings.SERIALIZERS.user_create
        elif self.action == "destroy" or (
                self.action == "me" and self.request and self.request.method == "DELETE"
        ):
            return settings.SERIALIZERS.user_delete
        elif self.action == "activation":
            return users.serializers.ActivationSerializer
        elif self.action == "resend_activation":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password":
            return settings.SERIALIZERS.password_reset
        elif self.action == "reset_password_confirm":
            if settings.PASSWORD_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.password_reset_confirm_retype
            return settings.SERIALIZERS.password_reset_confirm
        elif self.action == "set_password":
            if settings.SET_PASSWORD_RETYPE:
                return settings.SERIALIZERS.set_password_retype
            return settings.SERIALIZERS.set_password
        elif self.action == "set_username":
            if settings.SET_USERNAME_RETYPE:
                return settings.SERIALIZERS.set_username_retype
            return settings.SERIALIZERS.set_username
        elif self.action == "reset_username":
            return settings.SERIALIZERS.username_reset
        elif self.action == "reset_username_confirm":
            if settings.USERNAME_RESET_CONFIRM_RETYPE:
                return settings.SERIALIZERS.username_reset_confirm_retype
            return settings.SERIALIZERS.username_reset_confirm
        elif self.action == "me":
            return settings.SERIALIZERS.current_user

        return self.serializer_class

    @action(["post"], detail=False)
    def activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.user
        user.is_active = True
        user.save()

        signals.user_activated.send(
            sender=self.__class__, user=user, request=self.request
        )

        if settings.SEND_CONFIRMATION_EMAIL:
            context = {"user": user}
            to = [get_user_email(user)]
            ConfirmationEmail(self.request, context).send(to)

        return Response(status=status.HTTP_200_OK, data={"message": "Ваш аккаунт активирован"})

    @action(["post"], detail=False)
    def resend_activation(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.get_user(is_active=False)

        if not settings.SEND_ACTIVATION_EMAIL or not user:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        context = {"user": user}
        to = [get_user_email(user)]
        ActivationEmail(self.request, context).send(to)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer, *args, **kwargs):
        user = serializer.save(*args, **kwargs)
        signals.user_registered.send(
            sender=self.__class__, user=user, request=self.request
        )

        context = {"user": user}
        to = [get_user_email(user)]
        if settings.SEND_ACTIVATION_EMAIL:
            ActivationEmail(self.request, context).send(to)
        elif settings.SEND_CONFIRMATION_EMAIL:
            ConfirmationEmail(self.request, context).send(to)
        return Response(data={"message": f"Мы отправим код подтверждения на адрес{to[0]}"
                                         f". Это нужно для, того, чтобы активировать вашу учетную запись"})

    def perform_update(self, serializer, *args, **kwargs):
        super().perform_update(serializer, *args, **kwargs)
        user = serializer.instance
        signals.user_updated.send(
            sender=self.__class__, user=user, request=self.request
        )

        # should we send activation email after update?
        if settings.SEND_ACTIVATION_EMAIL and not user.is_active:
            context = {"user": user}
            to = [get_user_email(user)]
            ActivationEmail(self.request, context).send(to)
