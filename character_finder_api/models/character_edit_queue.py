from django.db import models


class CharacterEditQueue(models.Model):
    base_character = models.ForeignKey("character", on_delete=models.CASCADE, related_name="base_char")
    new_character = models.ForeignKey("character", on_delete=models.CASCADE, related_name="new_char")
    reason = models.CharField(max_length=2000)
    approved = models.BooleanField()
