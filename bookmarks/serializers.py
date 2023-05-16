from rest_framework import serializers
from .models import ReadingBookMark, WillReadBookMark, FinishBookMark


class ReadingBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingBookMark
        fields = '__all__'


class WillReadBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = WillReadBookMark
        fields = '__all__'


class FinishBookMarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinishBookMark
        fields = '__all__'
