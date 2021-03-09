from django.db import models
from django.db.models.deletion import DO_NOTHING


class Fiction(models.Model):
    reader = models.ForeignKey("Reader", on_delete=DO_NOTHING)
    title = models.CharField(max_length=200)
    date_published = models.DateField()
    description = models.CharField(max_length=5000)
    media_type = models.ForeignKey("MediaType", on_delete=DO_NOTHING)
    genre = models.ForeignKey('Genre', on_delete=DO_NOTHING)
