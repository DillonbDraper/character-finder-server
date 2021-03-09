from django.db import models
from django.db.models.deletion import CASCADE


class CharacterFictionAssociation(models.Model):
    character = models.ForeignKey("character", models.CASCADE)
    work = models.ForeignKey("fiction", on_delete=models.CASCADE)
    series = models.ForeignKey('series', on_delete=models.CASCADE)
    description = models.CharField(max_length=2000)
