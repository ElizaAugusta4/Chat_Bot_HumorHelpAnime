from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from.models import Anime, UserHumor

@login_required
def recommend_anime(request):
    user = request.user
    user_humor = UserHumor.objects.get(user=user)
    animes = Anime.objects.filter(humor=user_humor.humor_preference)
    return render(request, 'animes/recommendations.html', {'animes': animes})
