# from django.urls import path
# from . import views


# urlpatterns = [
#     path('', views.recommend_top, name='recomendar_animes'),
#     path('', views.recommend_genre, name='animes'),
#     path('', views.RecommendView, name='recomendar'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.recommend_animes, name='recomendar_animes'),
]
