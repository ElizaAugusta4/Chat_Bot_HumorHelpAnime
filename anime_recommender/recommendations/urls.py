from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='index'),
    path('recommend/', views.get_anime_by_genre, name='recommend'),
    path('recommend', views.get_anime_by_genre, name='recommendations')
]
