from rest_framework import generics
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark
from .serializers import ReadingBookMarkSerializer, WillReadBookMarkSerializer, FinishBookMarkSerializer


class ReadingBookMarkAPIView(generics.ListCreateAPIView):
    queryset = ReadingBookMark.objects.all()
    serializer_class = ReadingBookMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class WillReadBookMarkAPIView(generics.ListCreateAPIView):
    queryset = WillReadBookMark.objects.all()
    serializer_class = WillReadBookMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FinishBookMarkAPIView(generics.ListCreateAPIView):
    queryset = FinishBookMark.objects.all()
    serializer_class = FinishBookMarkSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)