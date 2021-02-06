from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True)
    def __str__(self):
        return self.name