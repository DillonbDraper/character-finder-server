from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.lookups import IsNull


class Author(models.Model):
    reader = models.ForeignKey("reader", on_delete=DO_NOTHING)
    name = models.CharField(max_length=20)
    bio = models.CharField(max_length=1000)
    born_on = models.DateField()
    died_on = models.DateField(blank=True)