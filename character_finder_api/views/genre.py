from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import serializers
from character_finder_api.models import Genre

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('id', 'name', )


class Genres(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                GenericViewSet):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()

    def create(self, request):
        genre = Genre()
        genre.name = request.data['name']
        user = request.auth.user

        if user.is_staff is True:
            try:
                genre.save()
                serializer = GenreSerializer(
                    genre, context={'request': request})
                return Response(serializer.data)
            except ValidationError as ex:
                return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"reason": "This is an admin only action"}, status=status.HTTP_401_UNAUTHORIZED)



