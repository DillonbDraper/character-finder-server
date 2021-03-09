from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.lookups import IsNull


class Genre(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    image = ImageField(IsNull=True)

