from django.db import models
from django.db.models.deletion import DO_NOTHING


class Author(models.Model):
    reader = models.ForeignKey("Reader", on_delete=DO_NOTHING)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=1000)
    born_on = models.DateField()
    died_on = models.DateField(blank=True, null=True)

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
    def series(self):
        return self.series

    @series.setter
    def series(self, value):
        self.__series = value
        