from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.lookups import IsNull


class Fiction(models.Model):
    reader = models.ForeignKey("Reader", on_delete=DO_NOTHING)
    title = models.CharField(max_length=200)
    image = models.ImageField(IsNull=True)
    date_published = models.DateField()
    author = models.ForeignKey("Author", on_delete=DO_NOTHING)
    description = models.CharField(max_length=5000)
    media_type = models.ForeignKey("MediaType", on_delete=DO_NOTHING)
