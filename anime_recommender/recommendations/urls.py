from django.urls import path
from . import views
from .views import RecommendView

urlpatterns = [
    path('', views.recommend_top, name='recomendar_animes'),
    path('', views.recommend_genre, name='recomendar_animes'),
    path('', RecommendView.as_view(), name='recomendar_animes'),
]