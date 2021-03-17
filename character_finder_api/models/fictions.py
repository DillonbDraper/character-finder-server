from django.db import models
from django.db.models.deletion import DO_NOTHING


class Fiction(models.Model):
    reader = models.ForeignKey("Reader", on_delete=DO_NOTHING)
    title = models.CharField(max_length=200)
    date_published = models.DateField()
    description = models.CharField(max_length=5000)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)

    @property
    def characters(self):
        return self.__characters

    @characters.setter
    def characters(self, value):
        self.__characters = value

    @property
    def creators(self):
        return self.__creators

    @creators.setter
    def creators(self, value):
        self.__creators = value

    @property
    def series(self):
        return self.__series

    @series.setter
    def series(self, value):
        self.__series = value