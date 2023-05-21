from kitepkana.books.models import Books
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def synchronize_books(request):
    web_app_books = request.data.get('web_app_books', [])
    mobile_app_books = request.data.get('mobile_app_books', [])

    web_app_book_ids = [book['id'] for book in web_app_books]
    mobile_app_book_ids = [book['id'] for book in mobile_app_books]

    web_app_only_books = Books.objects.filter(id__in=web_app_book_ids).exclude(id__in=mobile_app_book_ids)

    mobile_app_only_books = Books.objects.filter(id__in=mobile_app_book_ids).exclude(id__in=web_app_book_ids)

    for book in web_app_books:
        if book['id'] in mobile_app_book_ids:

            Books.objects.filter(id=book['id']).update(title=book['title'], author=book['pages'])

    for book in mobile_app_only_books:

        Books.objects.create(title=book['title'], author=book['pages'])

    return Response({'message': 'Books synchronized successfully'})

