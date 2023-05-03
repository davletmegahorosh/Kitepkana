from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Books, Review
from .serializers import BookSerializer, ReviewSerializer


class CatalogApiView(ListCreateAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class CatalogDetailApiView(RetrieveUpdateDestroyAPIView):
    queryset = Books.objects.all()
    serializer_class = BookSerializer


class ReviewApiView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = \
        ReviewSerializer


