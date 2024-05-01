from django.db import models
from django.contrib.auth.models import User

class Anime(models.Model):
    title = models.CharField(max_length=200)
    humor = models.CharField(max_length=50)  # Exemplo de humor: "Humorístico", "Serio", etc.
    description = models.TextField()

    def __str__(self):
        return self.title

class UserHumor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    humor_preference = models.CharField(max_length=50)  # Exemplo de humor: "Humorístico", "Serio", etc.

    def __str__(self):
        return self.user.username