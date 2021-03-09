from django.db import models


class CharacterFictionAssociation(models.Model):
    character = models.ForeignKey("Character", on_delete=models.CASCADE)
    fiction = models.ForeignKey("Fiction", on_delete=models.CASCADE)
    series = models.ForeignKey('Series', on_delete=models.CASCADE, blank=True, null=True)