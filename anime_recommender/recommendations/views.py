from django.shortcuts import render, redirect
from .models import UserPreference
import requests
from django.views import View

def recommend_genre(request):
    anime_list = []
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

def recommend_top(request):
   if not request.method == 'POST':
        url = 'https://graphql.anilist.co'
        query = """
               query{
                  Page(page:1,perPage:1000){ 
                       media(type:ANIME, sort: POPULARITY_DESC) {
                           title {
                               romaji
                               english
                           }
                           popularity
                           genres
                           coverImage {
                               large
                           }
                       }
                   }
               }
               """
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json={'query': query}, headers=headers)
        data = response.json()
        anime_list = []

        for anime in data['data']['Page']['media']:
            title = anime["title"]["romaji"]
            popularity = anime["popularity"]
            genres = anime["genres"]
            image_url = anime["coverImage"]["large"]

            anime_list.append({
                "images_jpg": image_url,
                "title": title,
                "genres": genres,
                "popularity": popularity
            })

        # Ordenar a lista de animes por popularidade em ordem decrescente
        anime_list.sort(key=lambda x: x['popularity'], reverse=True)

        # Retornar os 5 primeiros animes
        return render(request, 'recommend.html', {'animes': anime_list[:5]})
   else:
        return render(request, 'recommend.html')
      

def RecommendView(request): 
    stage = request.session.get('stage', None)
    if stage is None:
      stage = request.session['stage'] = 'response_greeting'
      message = 'Olá, tudo bem?'
    elif stage == 'response_greeting':
      message = 'Qual gênero de animes você gosta?'
      stage = request.session['stage'] = 'ask_genre'
    else:
      message = 'Lista de Animes:'
      stage = request.session['stage'] = None
    return render(request, 'recommend.html', {'message': message, 'stage': stage})
