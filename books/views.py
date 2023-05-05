from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Books
from .serializers import BookSerializer


class CatalogApiView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class CatalogDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer
