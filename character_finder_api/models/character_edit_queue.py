from django.db import models
from django.db.models.deletion import DO_NOTHING
from django.db.models.lookups import IsNull


class CharacterEditQueue(models.Model):
    base_character = models.ForeignKey("character", on_delete=models.CASCADE)
    new_character = models.ForeignKey("character", on_delete=models.CASCADE)
    approved = models.BooleanField()
