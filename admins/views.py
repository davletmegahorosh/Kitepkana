from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from books.models import Books, Authors, Genres
from admins.serializers import AdminPanelSerializer
from rest_framework.response import Response
from rest_framework import permissions


@extend_schema_view(
    get = extend_schema(
        summary='Метод для получения всех авторов, жанров, книг'
    )
)
class AdminPanelView(ListAPIView):
    serializer_class = AdminPanelSerializer
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, **kwargs):
        books = Books.objects.all()
        authors = Authors.objects.all()
        genres = Genres.objects.all()

        serializer_context = {
            'request': request,
        }

        serializer = AdminPanelSerializer({
            'books': books,
            'authors': authors,
            'genres': genres,

        }, context=serializer_context)

        return Response(serializer.data)
