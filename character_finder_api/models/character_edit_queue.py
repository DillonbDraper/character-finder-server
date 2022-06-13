from django.db import models


class CharacterEditQueue(models.Model):
    base_character = models.ForeignKey("character", on_delete=models.CASCADE, related_name="base_char")
    new_character = models.ForeignKey("character", on_delete=models.CASCADE, related_name="new_char")
    reader = models.ForeignKey("reader", on_delete=models.CASCADE, default=1)
    reason = models.CharField(max_length=2000)
    approved = models.BooleanField(null=True)
