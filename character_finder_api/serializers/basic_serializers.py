from character_finder_api.permissions import UserPermission
from character_finder_api.models import Author, Character, Series, Fiction
from rest_framework import serializers


class BasicCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        depth = 1
        fields = ( 'id', 'name', 'public_version',)

class BasicSeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = ( 'id', 'title', )

class BasicAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        depth = 1
        fields = ( 'id', 'name', )

class BasicFictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fiction
        depth = 1
        fields = ( 'id', 'title', )
