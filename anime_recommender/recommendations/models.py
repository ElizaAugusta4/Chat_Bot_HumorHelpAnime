from django.db import models


class UserPreference(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.genre


class Genero(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Anime(models.Model):
    title = models.CharField(max_length=255)
    generos = models.ManyToManyField(Genero)
    popularidade = models.IntegerField(default=0)
    sinopse = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
