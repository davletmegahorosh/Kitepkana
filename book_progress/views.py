from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from book_progress.models import BookProgress
from book_progress.serializers import BookProgressSerializer


@api_view(['GET', 'PUT'])
def book_progress(request, book_id):
    try:
        progress = BookProgress.objects.get(user=request.user, book_id=book_id)
    except BookProgress.DoesNotExist:
        return Response({'error': 'Book progress not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookProgressSerializer(progress)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = BookProgressSerializer(progress, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

