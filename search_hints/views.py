from rest_framework.views import APIView
from rest_framework.response import Response
from kitepkana.books.models import Books
from kitepkana.books.serializers import BookSerializer


class BookSearchHintsView(APIView):
    def get(self, request):
        search_term = request.GET.get('q', '')
        books = Books.objects.filter(title__icontains=search_term)[:10]

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

