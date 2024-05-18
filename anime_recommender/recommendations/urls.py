from django.urls import path
from .views import RecommendView
from .views import anime_view

urlpatterns = [
    path('recommend/', RecommendView.as_view(), name='recommend'),
    path('', anime_view, name='anime'),
]
