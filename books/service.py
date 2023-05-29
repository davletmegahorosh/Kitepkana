from django.shortcuts import get_object_or_404

from users.models import User


def get_client_username(request):
    user = get_object_or_404(User, username=request.user.username)
    return user.username

