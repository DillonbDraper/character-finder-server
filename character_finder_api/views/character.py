from character_finder_api.views import fiction
from character_finder_api.models.character_association import CharacterAssociation
from character_finder_api.serializers import BasicSeriesSerializer, BasicAuthorSerializer, BasicFictionSerializer
from django.core.exceptions import ValidationError
from rest_framework import status
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from django.db.models import Q
from character_finder_api.models import Character, Reader, CharacterFictionAssociation, Author, AuthorFictionAssociation, Series, CharacterEditQueue, Fiction
from rest_framework.decorators import action


class Characters(ViewSet):

    def create(self, request):
        character = Character()

        character.name = request.POST.get('name')
        character.image = request.FILES.get('image')
        character.reader = Reader.objects.get(user=request.auth.user)
        character.born_on = request.POST.get('born_on')
        character.died_on = request.POST.get('died_on')
        character.alias = request.POST.get('alias')
        character.age = request.POST.get('age')
        character.bio = request.POST.get('bio')

        if request.POST.get('edit') == True:
            character.public_version = False
        else:
            character.public_version = True

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

            character.associations = CharacterAssociation.objects.filter(
                char_one=character)
            if character.associations.count() > 0:
                serializer = FirstCharacterSerializer(
                    character, context={'request': request})
            else:
                character.associations = CharacterAssociation.objects.filter(
                    char_two=character)
                if character.associations.count() > 0:
                    serializer = SecondCharacterSerializer(
                        character, context={'request': request})

            if character.associations.count() == 0:
                serializer = FirstCharacterSerializer(
                    character, context={'request': request})

            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def list(self, request):
        characters = Character.objects.filter(public_version=True)

        name = self.request.query_params.get('name', None)
        fiction = self.request.query_params.get('fiction', None)
        author = self.request.query_params.get('author', None)
        series = self.request.query_params.get('series', None)

        if name is not None:
            characters = characters.filter(name__icontains=name)

        if fiction is not None:
            characters = characters.filter(
                fiction_char__fiction=int(fiction)).distinct()

        if series is not None:
            characters = characters.filter(
                fiction_char__series=int(series)).distinct()

        if author is not None:
            characters = characters.filter(
                fiction_char__fiction__author_fiction__author__id=int(author)).distinct()

        serializer = ListCharacterSerializer(
            characters, many=True, context={'request': request})
        return Response(serializer.data)

    def update(self, request, pk=None):

        character = Character.objects.get(pk=pk)
        reader = Reader.objects.get(user=request.auth.user)
        if request.auth.user.is_staff or character.reader == reader is True:

            if request.data['reset_queue']:

                relationships_to_wipe = CharacterFictionAssociation.objects.filter(
                    character=character)
                for relationship in relationships_to_wipe:
                    relationship.delete()

                intercharacter_relationships_to_wipe = CharacterAssociation.objects.filter(
                    Q(char_one=character) | Q(char_two=character))
                for relationship in intercharacter_relationships_to_wipe:
                    relationship.delete()

                queue_entry = CharacterEditQueue.objects.get(
                    new_character=character)
                queue_entry.approved = None
                queue_entry.save()

            character.born_on = request.data['born_on']
            character.died_on = request.data['died_on']
            character.alias = request.data['alias']
            character.age = request.data['age']
            character.bio = request.data['bio']
            character.image = request.FILES.get('image')
            character.reader = Reader.objects.get(pk=request.data['reader_id'])

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

    @action(methods=['post'], detail=True)
    def create_relationships(self, request, pk=None):

        if request.method == "POST":
            character = Character.objects.get(pk=pk)

            if 'characters' in request.data.keys():
                new_associate = Character.objects.get(
                    pk=request.data['characters']['id'])

                new_association = CharacterAssociation(
                    char_one=character, char_two=new_associate)
                new_association.description = request.data['description']
                new_association.save()

            if set(('series', 'fictions')).issubset(request.data):
                series = Series.objects.get(pk=request.data['series']['id'])
                fictions = request.data['fictions']
                for fic in fictions:
                    current_fiction = Fiction.objects.get(pk=fic['id'])
                    try:
                        char_fiction = CharacterFictionAssociation.objects.get(
                            character=character, fiction=current_fiction, series=series)
                        return Response({'request': "association already created"}, status=status.HTTP_406_NOT_ACCEPTABLE)
                    except CharacterFictionAssociation.DoesNotExist:
                        char_fiction = CharacterFictionAssociation()
                        char_fiction.character = character
                        char_fiction.fiction = current_fiction
                        char_fiction.series = series
                        char_fiction.save()

                return Response({}, status=status.HTTP_201_CREATED)

            elif 'fictions' in request.data.keys():
                fictions = request.data['fictions']
                for fiction in fictions:
                    current_fiction = Fiction.objects.get(pk=fiction['id'])
                    try:
                        char_fiction = CharacterFictionAssociation.objects.get(
                            character=character, fiction=current_fiction)
                    except CharacterFictionAssociation.DoesNotExist:
                        char_fiction = CharacterFictionAssociation()
                        char_fiction.character = character
                        char_fiction.fiction = current_fiction
                        char_fiction.save()

                        return Response({}, status=status.HTTP_201_CREATED)

            elif 'series' in request.data.keys():
                series = Series.objects.get(pk=request.data['series']['id'])

                try:
                    character_series_relationship = CharacterFictionAssociation.objects.get(
                        character=character, series=series)

                except CharacterFictionAssociation.DoesNotExist:
                    character_series = CharacterFictionAssociation()
                    character_series.character = character
                    character_series.series = series
                    character_series.save()

                return Response({}, status=status.HTTP_201_CREATED)

    @action(methods=['post'], detail=True)
    def edit_request(self, request, pk=None):

        if request.method == 'POST':
            base_character = Character.objects.get(pk=pk)
            reader = Reader.objects.get(user=request.auth.user)

            new_character = Character()

            new_character.name = request.POST.get('name')
            new_character.image = request.FILES.get('image')
            new_character.reader = reader
            new_character.born_on = request.POST.get('born_on')
            new_character.died_on = request.POST.get('died_on')
            new_character.alias = request.POST.get('alias')
            new_character.age = request.POST.get('age')
            new_character.bio = request.POST.get('bio')
            new_character.public_version = False

            try:
                check_queue = CharacterEditQueue.objects.get(
                    base_character=base_character, reader=reader)
                return Response({"request": "You already have an entry in the edit queue for this character"}, status=status.HTTP_406_NOT_ACCEPTABLE)

            except CharacterEditQueue.DoesNotExist:

                new_character.save()

                queue_entry = CharacterEditQueue()
                queue_entry.base_character = base_character
                queue_entry.reader = reader
                queue_entry.new_character = new_character
                if queue_entry.approved is not None:
                    queue_entry.approved = None
                queue_entry.save()

                serializer = GenericCharacterSerializer(
                    new_character, context={'request': request})
                return Response(serializer.data)

    @action(methods=['get'], detail=True)
    def check_for_match(self, request, pk=None):

        if request.method == 'GET':
            new_character = Character.objects.get(pk=pk)
            reader = new_character.reader

            try:
                edit_queue_entry = CharacterEditQueue.objects.get(
                    new_character=new_character, reader=reader)
                base_version = edit_queue_entry.base_character

                base_version.associations = CharacterAssociation.objects.filter(
                    char_one=base_version)
                if base_version.associations.count() > 0:
                    serializer = FirstCharacterSerializer(
                        base_version, context={'request': request})
                else:
                    base_version.associations = CharacterAssociation.objects.filter(
                        char_two=base_version)
                    if base_version.associations.count() > 0:
                        serializer = SecondCharacterSerializer(
                            base_version, context={'request': request})

                if base_version.associations.count() == 0:
                    serializer = FirstCharacterSerializer(
                        base_version, context={'request': request})

                return Response(serializer.data)

            except CharacterEditQueue.DoesNotExist:
                return Response({"response": "No match currently in edit queue"}, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return HttpResponseServerError(ex)

    @action(methods=['get'], detail=True)
    def check_for_match_original(self, request, pk=None):

        if request.method == 'GET':
            reader = Reader.objects.get(user=request.auth.user)
            base_character = Character.objects.get(pk=pk)

            try:
                edit_queue_entry = CharacterEditQueue.objects.get(
                    base_character=base_character, reader=reader)
                new_character = edit_queue_entry.new_character

                new_character.associations = CharacterAssociation.objects.filter(
                    char_one=new_character)
                if new_character.associations.count() > 0:
                    serializer = FirstCharacterSerializer(
                        new_character, context={'request': request})
                else:
                    new_character.associations = CharacterAssociation.objects.filter(
                        char_two=new_character)
                    if new_character.associations.count() > 0:
                        serializer = SecondCharacterSerializer(
                            new_character, context={'request': request})

                if new_character.associations.count() == 0:
                    serializer = FirstCharacterSerializer(
                        new_character, context={'request': request})

                return Response(serializer.data)

            except CharacterEditQueue.DoesNotExist:
                return Response({}, status=status.HTTP_204_NO_CONTENT)
            except Exception as ex:
                return HttpResponseServerError(ex)

    @action(methods=['put', 'delete'], detail=True)
    def decide_edit(self, request, pk=None):
        reader = Reader.objects.get(user=request.auth.user)
        base_character = Character.objects.get(pk=pk)
        new_character = Character.objects.get(pk=request.data['id'])

        if reader.user.is_staff is False:
            return Response({"warning": "Only admins may perform this action"}, status=status.HTTP_401_UNAUTHORIZED)
        if request.method == 'PUT':

            try:
                queue_entry = CharacterEditQueue.objects.get(
                    base_character=base_character, new_character=new_character)
                base_character.name = new_character.name
                base_character.alias = new_character.alias
                base_character.born_on = new_character.born_on
                base_character.died_on = new_character.died_on
                base_character.bio = new_character.bio
                base_character.image = new_character.image

                base_character_associations = CharacterFictionAssociation.objects.filter(character=base_character)
                for association in base_character_associations:
                    association.delete()

                base_character_associations_with_chars = CharacterAssociation.objects.filter(char_one=base_character)
                for association in base_character_associations_with_chars:
                    association.delete()

                base_character.save()
                new_character.delete()

                return Response({"Message": "Edit successful"}, status=status.HTTP_200_OK)
            except Exception as ex:
                return HttpResponseServerError(ex)

        elif request.method == 'DELETE':
            try:
                queue = CharacterEditQueue.objects.get(
                    base_character=base_character, new_character=new_character, reader=reader)
                queue.approved = False
                queue.save()

                return Response({"Message": "Edit removed from consideration"}, status=status.HTTP_200_OK)

            except Exception as ex:
                return HttpResponseServerError(ex)

    @action(methods=['get'], detail=False)
    def unapproved(self, request):
        unapproved_characters = Character.objects.filter(
            public_version=False).exclude(new_char__approved=False)

        name = self.request.query_params.get('name', None)
        fic = self.request.query_params.get('fiction', None)
        author = self.request.query_params.get('author', None)
        series = self.request.query_params.get('series', None)

        if name is not None:
            unapproved_characters = unapproved_characters.filter(
                name__icontains=name)

        if fic is not None:
            unapproved_characters = unapproved_characters.filter(
                fiction_char__fiction=int(fic))

        if series is not None:
            unapproved_characters = unapproved_characters.filter(
                fiction_char__series=int(series))

        if author is not None:
            unapproved_characters = unapproved_characters.filter(
                fiction_char__fiction__author_fiction__author__id=int(author))

        serializer = ListCharacterSerializer(
            unapproved_characters, many=True, context={'request': request})
        return Response(serializer.data)

    @action(methods=['delete'], detail=True)
    def destroy_all_personal_versions(self, request, pk=None):
        if request.auth.user.is_staff:
            personal_versions = Character.objects.filter(
                new_char__base_character__id=pk)
            for character in personal_versions:
                character.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"Warning": "Only admins may access this function"}, status=status.HTTP_403_FORBIDDEN)


class AssociatedCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ('id', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio',)


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

    works = BasicFictionSerializer(many=True)
    series = BasicSeriesSerializer(many=True)
    creators = BasicAuthorSerializer(many=True)
    associations = FirstAssociationSerializer(many=True)

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio',
                  'public_version', 'works', 'series', 'creators', 'associations', 'image')


class SecondCharacterSerializer(serializers.ModelSerializer):

    works = BasicFictionSerializer(many=True)
    series = BasicSeriesSerializer(many=True)
    creators = BasicAuthorSerializer(many=True)
    associations = SecondAssociationSerializer(many=True)

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias', 'bio',
                  'public_version', 'works', 'series', 'creators', 'associations', 'image')


class GenericCharacterSerializer(serializers.ModelSerializer):
    works = BasicFictionSerializer(many=True)

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'reader', 'name', 'age', 'born_on', 'died_on', 'alias',
                  'bio', 'public_version', 'works', 'series', 'creators', 'image', )


class ListCharacterSerializer(serializers.ModelSerializer):

    works = BasicFictionSerializer(many=True)
    series = BasicSeriesSerializer(many=True)
    creators = BasicAuthorSerializer(many=True)

    class Meta:
        model = Character
        depth = 1
        fields = ('id', 'name', 'alias', 'public_version',
                  'works', 'series', 'creators', 'reader')
