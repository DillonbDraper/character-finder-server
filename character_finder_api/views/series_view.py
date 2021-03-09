from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from character_finder_api.models import Series
from character_finder_api.views.genre import GenreSerializer


class SeriesView(ViewSet):

    def create(self, request):
        series = Series()

        series.label = request.data['label']

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
            # `pk` is a parameter to this function, and
            # Django parses it from the URL route parameter
            #   http://localhost:8000/categories/2
            #
            # The `2` at the end of the route becomes `pk`
            post = Series.objects.get(pk=pk)
            serializer = SeriesSerializer(post, context={'request': request})
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
        series.label = request.data['label']

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

    class Meta:
        model = Series
        genre = GenreSerializer
        depth = 1
        fields = ('id', 'title', 'description', 'genre', )
