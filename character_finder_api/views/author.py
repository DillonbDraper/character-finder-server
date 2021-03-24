from character_finder_api.serializers.basic_serializers import BasicFictionSerializer, BasicSeriesSerializer, BasicCharacterSerializer
from character_finder_api.models.series import Series
from character_finder_api.models.fictions import Fiction
from character_finder_api.models.characters import Character
from character_finder_api.models import Author, Reader, AuthorFictionAssociation, CharacterFictionAssociation
from rest_framework import serializers, status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.http import HttpResponseServerError
from character_finder_api.permissions import UserPermission



class ExtendedAuthorSerializer(serializers.ModelSerializer):
    characters = BasicCharacterSerializer(many=True)
    works = BasicFictionSerializer(many=True)
    series = BasicSeriesSerializer(many=True)
    class Meta:
        model = Author
        fields = ('id', 'reader', 'name', 'born_on', 'died_on', 'bio', 'characters', 'works', 'series')

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('id', 'reader', 'name', 'born_on', 'died_on', 'bio',)

class Authors(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [UserPermission]

    def create(self, request):
        author = Author()

        author.name = request.data['name']
        author.reader = Reader.objects.get(user=request.auth.user)
        author.born_on = request.data['born_on']

        if author.died_on and author.died_on != "":
            author.died_on = request.data['died_on']
        author.bio = request.data['bio']
        
        try:
            author.save()
            serializer = AuthorSerializer(
                author, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single character
        Returns:
            Response -- JSON serialized character instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/categories/2
            #
            # The `2` at the end of the route becomes `pk`
            author = Author.objects.get(pk=pk)

            author.characters = Character.objects.filter(fiction_char__fiction__author_fiction__author=author).distinct()
            author.works = Fiction.objects.filter(author_fiction__author=author).distinct()
            author.series = Series.objects.filter(char_series__fiction__author_fiction__author=author).distinct()
            
            serializer = ExtendedAuthorSerializer(author, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)        
