from django.shortcuts import render, redirect
from .forms import UserPreference
from .services import get_anime_by_genre
import requests


def recommend(request):
    if request.method == 'POST':
        genre = request.POST['genre']
        animes = get_anime_by_genre(genre)
        return render(request, 'recommend.html', {'animes': animes})
    else:
        return render(request, 'recommend.html')


def get_anime_by_genre(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        user_preference = UserPreference()
        user_preference.genre = genre
        user_preference.save()

        url = "https://api.jikan.moe/v4/anime"
        params = {"genre": genre}
        response = requests.get(url, params=params)
        print(response.url)
        data = response.json()
        print(genre)




        anime_list = []

        for anime in data['data']:
            genres_list = anime['genres']
            genres_name = [genre['name'] for genre in genres_list]
            images_list = anime['images']
            if 'jpg' in images_list:
                jpg_image_url = images_list['jpg']['image_url']

            anime_list.append({
                "images_jpg": jpg_image_url,
                "title": anime["title"],
                "genres": genres_name,
                "score": anime["score"]
            })
            anime_list = anime_list[:5]

        return render(request, 'recommend.html', {'animes': anime_list})
    else:
        return render(request, 'recommend.html')


class RecommendView():
    def get(self, request):
        stage = request.session.get('stage', 'greeting')
        if stage == 'greeting':
            message = 'Olá, tudo bem?'
        elif stage == 'ask_genre':
            message = 'Qual gênero de animes você gosta?'
        else:
            message = 'Desculpe, não entendi.'
        return render(request, 'recommend.html', {'message': message})


def save_user_preference(request):
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = UserPreferenceForm()
    return render(request, 'recommend.html', {'form': form})
