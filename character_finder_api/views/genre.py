from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import serializers
from character_finder_api.models import Genre

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', )

class Genres(ModelViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

