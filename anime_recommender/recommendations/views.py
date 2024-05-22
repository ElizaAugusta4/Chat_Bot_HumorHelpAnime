from django.shortcuts import render, redirect
from .models import UserPreference
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

        url = 'https://graphql.anilist.co'
        query = """
        query ($genre: String) {
          Page (page: 1, perPage: 5) {
            media (genre: $genre, type: ANIME) {
              title {
                romaji
                english
                native
              }
              genres
              coverImage {
                large
              }
            }
          }
        }
        """
        variables = {
            'genre': genre
        }

        response = requests.post(url, json={'query': query, 'variables': variables})
        data = response.json()

        anime_list = []

        for anime in data['data']['Page']['media']:
            title = anime["title"]["romaji"]
            genres = anime["genres"]
            image_url = anime["coverImage"]["large"]

            anime_list.append({
                "images_jpg": image_url,
                "title": title,
                "genres": genres,
            })

            # Create and save a UserPreference instance
            user_preference = UserPreference.objects.filter(
                genre=genre,
                title=title
            )

            # If it doesn't exist, create it
            if not user_preference.exists():
                UserPreference.objects.create(genre=genre, title=title)


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


