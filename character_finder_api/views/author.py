from character_finder_api.models.characters import Character
from character_finder_api.models import Author, Reader
from rest_framework import serializers, status
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from django.http import HttpResponseServerError
from character_finder_api.permissions import UserPermission

class GenericCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio', 'public_version',)


class AuthorSerializer(serializers.ModelSerializer):
    characters = GenericCharacterSerializer(many=True)
    class Meta:
        model = Author
        fields = ('id', 'reader', 'name', 'born_on', 'died_on', 'bio', 'characters')

class Authors(ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [UserPermission]

    def create(self, request):
        author = Author()

        author.name = request.data['name']
        author.reader = Reader.objects.get(user=request.auth.user)
        author.born_on = request.data['born_on']
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

            author.characters = Character.objects.filter(fiction_char__fiction__author_fiction__author=author)
            
            serializer = AuthorSerializer(author, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)
        
