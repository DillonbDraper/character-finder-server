from character_finder_api.models.authors import Author
from character_finder_api.models.character_association import CharacterAssociation
from character_finder_api.views.series_view import SeriesSerializer
from character_finder_api.views.fiction import FictionSerializer
from character_finder_api.views.author import AuthorSerializer
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from django.db.models import Q
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from character_finder_api.models import Character, Series, Reader, Author, Fiction
from character_finder_api.views.genre import GenreSerializer


class Characters(ViewSet):

    def create(self, request):
        character = Character()

        character.name = request.data['name']
        character.reader = Reader.objects.get(user=request.auth.user)
        character.born_on = request.data['born_on']
        character.died_on = request.data['died_on']
        character.alias = request.data['alias']
        character.age = request.data['age']
        character.bio = request.data['bio']
        
        if request.auth.user.is_staff is True:
            character.public_version = True
        else:
            character.public_version = False

        try:
            character.save()
            serializer = GenericCharacterSerializer(
                character, context={'request': request})
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
            character = Character.objects.get(pk=pk)

            character.associations = CharacterAssociation.objects.filter(char_one=character)
            if character.associations.count() > 0:
                serializer = FirstCharacterSerializer(character, context={'request': request})
            else:
                character.associations = CharacterAssociation.objects.filter(char_two=character)
                if character.associations.count() > 0:
                    serializer = SecondCharacterSerializer(character, context={'request': request})



            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        characters = Character.objects.all()

        name = self.request.query_params.get('name', None)
        fiction = self.request.query_params.get('fiction', None)
        author = self.request.query_params.get('author', None)
        series = self.request.query_params.get('series', None)
        alias = self.request.query_params.get('alias', None)

        if name is not None:
            characters = Character.objects.filter(name__icontains=name)
        
        if alias is not None:
            characters = Character.objects.filter(alias__icontains=alias)
        
        if fiction is not None:
            characters = Character.objects.filter(fiction_char__fiction=int(fiction))

        if series is not None:
            characters = Character.objects.filter(fiction_char__series=int(series))

        if author is not None:
            characters=Character.objects.filter(fiction_char__fiction__author_fiction__author__name__icontains=author)



        serializer = GenericCharacterSerializer(
            characters, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

        if request.auth.user.is_staff is True:
                
            character = Character.objects.get(pk=pk)
            character.reader = Reader.objects.get(user=request.auth.user)
            character.born_on = request.data['born_on']
            character.died_on = request.data['died_on']
            character.alias = request.data['alias']
            character.age = request.data['age']
            character.bio = request.data['bio']

            character.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        else: 
            return Response({"message": "Only staff may update characters directly"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):

        if request.auth.user.is_staff is True:

            try:
                character = Character.objects.get(pk=pk)
                character.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Character.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            return Response({"message": "Only staff may delete characters directly"}, status=status.HTTP_401_UNAUTHORIZED)

class AssociatedCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ('name', 'age', 'born_on', 'died_on', 'alias', 'bio',)

class FirstAssociationSerializer(serializers.ModelSerializer):

    char_two = AssociatedCharacterSerializer(many=False)
    class Meta:
        model = CharacterAssociation
        fields = ('char_two', 'description',)

class SecondAssociationSerializer(serializers.ModelSerializer):

    char_one = AssociatedCharacterSerializer(many=False)
    class Meta:
        model = CharacterAssociation
        fields = ('char_one', 'description',)

class FirstCharacterSerializer(serializers.ModelSerializer):

    works = FictionSerializer(many=True)
    series = SeriesSerializer(many=True)
    creators = AuthorSerializer(many=True)
    associations = FirstAssociationSerializer(many=True)

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio', 'public_version','works', 'series', 'creators', 'associations')

class SecondCharacterSerializer(serializers.ModelSerializer):

    works = FictionSerializer(many=True)
    series = SeriesSerializer(many=True)
    creators = AuthorSerializer(many=True)
    associations = SecondAssociationSerializer(many=True)

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio', 'public_version','works', 'series', 'creators', 'associations')


class GenericCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio', 'public_version',)