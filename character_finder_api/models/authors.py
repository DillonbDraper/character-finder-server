from django.db import models
from django.db.models.deletion import DO_NOTHING


class Author(models.Model):
    reader = models.ForeignKey("Reader", on_delete=DO_NOTHING)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=1000)
    born_on = models.DateField()
    died_on = models.DateField(blank=True)