from character_finder_api.models.character_association import CharacterAssociation
from character_finder_api.models.series import Series
from character_finder_api.models.fictions import Fiction
from character_finder_api.models.authors import Author
from django.db import models
from django.db.models.deletion import DO_NOTHING


class Character(models.Model):
    reader = models.ForeignKey("reader", on_delete=DO_NOTHING)
    age = models.CharField(max_length=20)
    born_on = models.CharField(max_length=50)
    died_on = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=200)
    bio = models.CharField(max_length=5000)
    public_version = models.BooleanField()

    @property
    def creators(self):
        creators = Author.objects.filter(fiction_author__fiction__char_fiction__character=self).distinct()
        return creators
    
    @property
    def works(self):
        works = Fiction.objects.filter(char_fiction__character=self).distinct()
        if len(works) == 0:
            return ""
        else: 
            return works

    @property
    def associations(self):
        return self.__associations

    @associations.setter
    def associations(self, value):
        self.__associations = value


    @property
    def series(self):
        series = Series.objects.filter(char_series__character=self).distinct()
        if len(series) == 0:
            return ""
        else:
            return series
    