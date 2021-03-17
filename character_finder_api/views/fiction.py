from character_finder_api.models.fiction_characters import CharacterFictionAssociation
from character_finder_api.models.author_fiction import AuthorFictionAssociation
from character_finder_api.models.authors import Author
from character_finder_api.serializers.basic_serializers import BasicAuthorSerializer, BasicCharacterSerializer, BasicSeriesSerializer
from character_finder_api.models.series import Series
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework.decorators import action
from character_finder_api.models import Character, Genre, Reader, Fiction
from character_finder_api.views.genre import GenreSerializer


class Fictions(ViewSet):

    def create(self, request):
        fiction = Fiction()

        fiction.title = request.data['title']
        fiction.reader = Reader.objects.get(user=request.auth.user)
        fiction.description = request.data['description']
        fiction.date_published = request.data['date_published']
        fiction.genre = Genre.objects.get(pk=request.data['genre']['id'])

        try:
            fiction.save()
            serializer = FictionSerializer(
                fiction, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single fiction
        Returns:
            Response -- JSON serialized fiction instance
        """
        try:
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/categories/2
            #
            # The `2` at the end of the route becomes `pk`
            fiction = Fiction.objects.get(pk=pk)
            fiction.characters = Character.objects.filter(
                fiction_char__fiction=fiction)
            fiction.creators = Author.objects.filter(
                fiction_author__fiction=fiction)
            fiction.series = Series.objects.filter(
                char_series__fiction=fiction)

            serializer = ExtendedFictionSerializer(
                fiction, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        fictions = Fiction.objects.all()

        serializer = FictionSerializer(
            fictions, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

        if request.auth.user.is_staff is True:

            fiction = Fiction.objects.get(pk=pk)
            fiction.title = request.data['title']
            fiction.description = request.data['description']
            fiction.date_published = request.data['date_published']
            fiction.genre = Genre.objects.get(pk=request.data['genre'])

            fiction.save()
            return Response({}, status=status.HTTP_204_NO_CONTENT)

        else:
            return Response({"message": "Only staff may update works of fiction directly"}, status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, pk=None):

        if request.auth.user.is_staff is True:

            try:
                fiction = Fiction.objects.get(pk=pk)
                fiction.delete()

                return Response({}, status=status.HTTP_204_NO_CONTENT)

            except Fiction.DoesNotExist as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

            except Exception as ex:
                return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        else:
            return Response({"message": "Only staff may delete works of fiction directly"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(methods=['post'], detail=True)
    def create_relationships(self, request, pk=None):

        if request.method == "POST":
            fiction = Fiction.objects.get(pk=pk)
            if 'author' in request.data.keys():
                author = Author.objects.get(pk=request.data['author']['id'])
                try:
                    author_work = AuthorFictionAssociation.objects.get(
                        author=author, fiction=fiction)

                except AuthorFictionAssociation.DoesNotExist:
                    author_work = AuthorFictionAssociation()
                    author_work.fiction = fiction
                    author_work.author = author
                    author_work.save()

                    if 'characters' in request.data.keys() or 'series' in request.data.keys():
                        pass
                    else: return Response({}, status=status.HTTP_201_CREATED) 


            if set(('series', 'characters')).issubset(request.data):
                series = Series.objects.get(pk=request.data['series']['id'])
                characters = request.data['characters']
                for character in characters:
                    char = Character.objects.get(pk=character['id'])
                    try:
                        char_fiction = CharacterFictionAssociation.objects.get(character=char, fiction=fiction, series=series)
                        return Response({'request': "association already created"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    except CharacterFictionAssociation.DoesNotExist:
                        char_fiction = CharacterFictionAssociation()
                        char_fiction.character = char
                        char_fiction.fiction = fiction
                        try: 
                            series_checker = CharacterFictionAssociation.objects.get(fiction=fiction, series=series)
                            char_fiction.save
                        except CharacterFictionAssociation.DoesNotExist: 
                            char_fiction.series = series
                            char_fiction.save()

                return Response({}, status=status.HTTP_201_CREATED)

            elif 'series' in request.data.keys():
                series = Series.objects.get(pk=request.data['series']['id'])
                try:
                    char_fiction = CharacterFictionAssociation.objects.get(
                        series=series, fiction=fiction)
                except CharacterFictionAssociation.DoesNotExist:
                    char_fiction = CharacterFictionAssociation()
                    char_fiction.fiction = fiction
                    char_fiction.series = series
                    char_fiction.save()

                    return Response({}, status=status.HTTP_201_CREATED)

            elif 'characters' in request.data.keys():
                for character in request.data['characters']:
                    char = Character.objects.get(pk=character['id'])
                    try:
                        char_fiction = CharacterFictionAssociation.objects.get(character=char, fiction=fiction)

                    except CharacterFictionAssociation.DoesNotExist:
                        char_fiction = CharacterFictionAssociation()
                        char_fiction.character = char
                        char_fiction.fiction = fiction
                        char_fiction.save()

                return Response({}, status=status.HTTP_201_CREATED)


class FictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fiction
        depth = 1
        fields = ('id', 'reader', 'title',
                  'date_published', 'description', 'genre',)


class ExtendedFictionSerializer(serializers.ModelSerializer):

    characters = BasicCharacterSerializer(many=True)
    creators = BasicAuthorSerializer(many=True)
    series = BasicSeriesSerializer(many=True)

    class Meta:
        model = Fiction
        depth = 1
        fields = ('id', 'reader', 'title', 'date_published',
                  'description', 'genre', 'creators', 'characters', 'series')
