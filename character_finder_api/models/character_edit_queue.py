from django.db import models


class CharacterEditQueue(models.Model):
    base_character = models.ForeignKey("character", on_delete=models.CASCADE)
    new_character = models.ForeignKey("character", on_delete=models.CASCADE)
    reason = models.CharField(max_length=2000)
    approved = models.BooleanField()
