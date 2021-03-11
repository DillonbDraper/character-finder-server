from django.db import models


class AuthorFictionAssociation(models.Model):
    author = models.ForeignKey("Author", on_delete=models.CASCADE, related_name="fiction_author")
    fiction = models.ForeignKey("Fiction", on_delete=models.CASCADE, related_name="author_fiction")
