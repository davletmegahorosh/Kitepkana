from rest_framework import serializers
from book_progress.models import BookProgress


class BookProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookProgress
        fields = ['user', 'book', 'current_page']
