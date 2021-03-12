from character_finder_api.views import character
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from character_finder_api.models import Series, Genre, Fiction, Author
from character_finder_api.serializers import BasicCharacterSerializer, BasicAuthorSerializer, BasicFictionSerializer
from character_finder_api.views.genre import GenreSerializer


class SeriesView(ViewSet):

    def create(self, request):
        series = Series()

        series.title = request.data['title']
        series.description = request.data['description']
        series.genre = Genre.objects.get(pk = request.data['genreId'])

        try:
            series.save()
            serializer = SeriesSerializer(
                series, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single series
        Returns:
            Response -- JSON serialized series instance
        """
        try:
            
            series = Series.objects.get(pk=pk)
            series.works = Fiction.objects.filter(char_fiction__series=series)
            series.creators = Author.objects.filter(fiction_author__fiction__char_fiction__series=series)
            serializer = ExtendedSeriesSerializer(series, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        categories = Series.objects.all()

        serializer = SeriesSerializer(
            categories, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

        series = Series.objects.get(pk=pk)
        series.title = request.data['title']
        series.genre = Genre.objects.get(pk=request.data['genreId'])

        series.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):

        try:
            series = Series.objects.get(pk=pk)
            series.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Series.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SeriesSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=False)


    class Meta:
        model = Series
        depth = 1
        fields = ('id', 'title', 'description', 'genre', )


class ExtendedSeriesSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(many=False)
    creators = BasicAuthorSerializer(many=True)
    # characters = BasicCharacterSerializer(many=True)
    works = BasicFictionSerializer(many=True)


    class Meta:
        model = Series
        depth = 1
        fields = ('id', 'title', 'description', 'genre', 'works', 'creators')