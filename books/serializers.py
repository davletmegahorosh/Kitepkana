from rest_framework import serializers
from .models import Books


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Books
        fields = '__all__'