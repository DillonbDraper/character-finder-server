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
