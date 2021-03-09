from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.lookups import IsNull


class Character(models.Model):
    reader = models.ForeignKey("reader", on_delete=DO_NOTHING)
    first_name = models.CharField(max_length=20)
    last_name = models.ImageField(IsNull=True)
    bio = models.CharField(max_length=50)
    born_on = models.DateField()
    died_on = models.DateField(max_length=50, IsNull=True)