from django.db import models
from django.db.models.fields.files import ImageField
from django.db.models.lookups import IsNull


class Reader(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = ImageField(IsNull=True)

