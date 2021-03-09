from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.lookups import IsNull


class Character(models.Model):
    reader = models.ForeignKey("reader", on_delete=DO_NOTHING)
    age = models.CharField(max_length=20)
    image = models.ImageField(IsNull=True)
    born_on = models.CharField(max_length=50)
    died_on = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    alias = models.CharField(max_length=200)
    bio = models.CharField(max_length=5000)
    public_version = models.BooleanField()
