from django.db import models


class CharacterFictionAssociation(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE, related_name="fiction_char")
    fiction = models.ForeignKey("Fiction", on_delete=models.CASCADE, related_name="char_fiction")
    series = models.ForeignKey('Series', on_delete=models.CASCADE, blank=True, null=True, related_name="char_series")