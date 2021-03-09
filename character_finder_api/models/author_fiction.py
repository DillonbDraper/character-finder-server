from django.db import models


class AuthorFictionAssociation(models.Model):
    author = models.ForeignKey("author", on_delete=models.CASCADE)
    work = models.ForeignKey("fiction", on_delete=models.CASCADE)
