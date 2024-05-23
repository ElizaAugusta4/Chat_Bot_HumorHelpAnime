from django.db import models

class UserPreference(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


class Anime(models.Model):
    title = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='anime_covers')
    view_count = models.IntegerField(default=0)
