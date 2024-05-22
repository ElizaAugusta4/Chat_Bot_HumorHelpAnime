from django.db import models

class UserPreference(models.Model):
    genre = models.CharField(max_length=100)
    title = models.CharField(max_length=200)


    def __str__(self):
        return f'Genre: {self.genre}, Title: {self.title}'