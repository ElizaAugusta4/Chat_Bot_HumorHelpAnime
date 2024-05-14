from django.db import models

class UserPreference(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre
