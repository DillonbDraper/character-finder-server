from django.db import models


class MediaType(models.Model):
    name = models.CharField(max_length=200)
