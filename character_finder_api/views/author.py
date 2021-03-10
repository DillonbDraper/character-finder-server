from character_finder_api.models import Author, Reader
from rest_framework import serializers, status
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import ValidationError
from rest_framework.response import Response
from character_finder_api.permissions import UserPermission

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
        author.died_on = request.data['died_on']
        author.bio = request.data['bio']
        
        try:
            author.save()
            serializer = AuthorSerializer(
                author, context={'request': request})
            return Response(serializer.data)
        except ValidationError as ex:
            return Response({"reason": ex.message}, status=status.HTTP_400_BAD_REQUEST)
