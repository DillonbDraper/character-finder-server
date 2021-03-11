from django.db import models
from django.db.models.deletion import DO_NOTHING


class Series(models.Model):
    title = models.CharField(max_length=300)
    description = models.CharField(max_length=2000)
    genre = models.ForeignKey("genre", on_delete=DO_NOTHING)
