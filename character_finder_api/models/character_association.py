from django.db import models
from django.db.models.deletion import CASCADE


class CharacterAssociation(models.Model):
    char_one = models.ForeignKey("character", on_delete=CASCADE, related_name='char_one')
    char_two = models.ForeignKey("character", on_delete=CASCADE, related_name='char_two')
    description = models.CharField(max_length=2000)
