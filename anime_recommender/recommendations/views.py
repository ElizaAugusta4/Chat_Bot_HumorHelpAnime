from django.shortcuts import render,redirect
from .models import UserPreference
import requests
import random

def recommend(request):
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
        return redirect('recommendations')


def get_anime_by_genre(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        genre = genre
        user_preference = UserPreference()
        user_preference.genre = genre
        user_preference.save()
        url = 'https://graphql.anilist.co'
        query = """
            query($genre: String) {
               Page(page:1,perPage:20){ 
                    media(genre: $genre, type:ANIME) {
                        title {
                            romaji
                            english
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

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        data = response.json()

        anime_list = []

        for anime in data['data']['Page']['media']:
            title = anime["title"]["romaji"]
            genres = anime["genres"]
            image_url = anime["coverImage"]["large"]

            anime_list.append({
                "images_jpg": image_url,
                "title": title,
                "genres": genres
            })

        return render(request, 'recommend.html', {'anime': anime_list})
    else:
        url = 'https://graphql.anilist.co'
        query = """
               query {
                  Page(page:1,perPage:20){ 
                       media(type:ANIME) {
                           title {
                               romaji
                               english
                           }
                           genres
                           coverImage {
                               large
                           }
                       }
                   }
               }
               """

        variables = {}

        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
        data = response.json()

        anime_list = []

        for anime in data['data']['Page']['media']:
            title = anime["title"]["romaji"]
            genres = anime["genres"]
            image_url = anime["coverImage"]["large"]

            anime_list.append({
                "images_jpg": image_url,
                "title": title,
                "genres": genres
            })
        
        user_preference = UserPreference.objects.filter(
          genre=genre,
          title=title
        )

        # If it doesn't exist, create it
        if not user_preference.exists():
          UserPreference.objects.create(genre=genre, title=title)

        # Selecione aleatoriamente 10 animes da lista
        random_animes = random.sample(anime_list, 10)

        return render(request, 'recommend.html', {'anime': random_animes})

      