from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_anime_by_genre, name='recommend'),
]