from django.db import models
from django.db.models.deletion import DO_NOTHING


class Series(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=2000)
    genre = models.ForeignKey("genre", on_delete=DO_NOTHING)

    @property
    def characters(self):
        return self.__characters

    @characters.setter
    def characters(self, value):
        self.__characters = value

    @property
    def works(self):
        return self.__works

    @works.setter
    def works(self, value):
        self.__works = value

    @property
    def creators(self):
        return self.__creators

    @creators.setter
    def creators(self, value):
        self.__creators = value