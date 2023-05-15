from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Вьюшка для того чтобы пользователь мог получать свои данные, а также
    изменять их
    """
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'


