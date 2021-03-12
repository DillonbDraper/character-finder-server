from character_finder_api.permissions import UserPermission
from character_finder_api.models import Author, Character, Series, Fiction
from rest_framework import serializers


class BasicCharacterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Character
        fields = ( 'id', 'name', 'public_version',)

class BasicSeriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Series
        fields = ( 'id', 'title', )

class BasicAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ( 'id', 'name', )

class BasicFictionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fiction
        fields = ( 'id', 'title', )
