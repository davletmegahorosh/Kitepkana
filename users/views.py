from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer

class ProfileRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    '''
    Вьюшка для того чтобы пользователь мог получать свои данные, а также
    изменять их
    '''
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'username'
