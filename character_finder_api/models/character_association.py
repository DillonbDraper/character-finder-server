from django.db import models
from django.db.models.deletion import CASCADE


class CharacterAssociation(models.Model):
    char_one = models.ForeignKey("character", on_delete=CASCADE)
    char_two = models.ForeignKey("character", on_delete=CASCADE)
    description = models.CharField(max_length=2000)
