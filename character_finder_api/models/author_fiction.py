from django.db import models


class AuthorFictionAssociation(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE)
    fiction = models.ForeignKey("Fiction", on_delete=models.CASCADE)
