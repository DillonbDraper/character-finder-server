from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from character_finder_api.models import Character, Genre, Reader, Fiction, MediaType
from character_finder_api.views.genre import GenreSerializer


class Fictions(ViewSet):

    def create(self, request):
        fiction = Fiction()

        fiction.title = request.data['title']
        fiction.reader = Reader.objects.get(user=request.auth.user)
        fiction.description = request.data['description']
        fiction.date_published = request.data['date_published']
        fiction.genre = Genre.objects.get(pk=request.data['genre'])
        fiction.media_type = MediaType.objects.get(pk=request.data['media_type'])
        
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
            serializer = FictionSerializer(fiction, context={'request': request})
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
            fiction.media_type = MediaType.objects.get(pk=request.data['media_type'])

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

class FictionSerializer(serializers.ModelSerializer):
    

    class Meta:
        model = Fiction
        depth = 1
        fields = ('id','reader', 'title', 'date_published', 'description', 'media_type', 'genre',)
