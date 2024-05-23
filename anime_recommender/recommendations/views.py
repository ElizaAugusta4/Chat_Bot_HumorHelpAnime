import random

import requests
from django.shortcuts import render, redirect
from .forms import UserPreference


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

        # Selecione aleatoriamente 10 animes da lista
        random_animes = random.sample(anime_list, 10)

        return render(request, 'recommend.html', {'anime': random_animes})



    '''if request.method == 'POST':
        genre = request.POST.get('genre')
        user_preference = UserPreference()
        user_preference.genre = genre
        user_preference.save()

        url = "https://api.jikan.moe/v4/anime/"
        params = {"genre": genre}
        response = requests.get(url, params)
        print(response.url)
        data = response.json()
        print(data)

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
            anime_list = anime_list[:15]

        return render(request, 'recommend.html', {'animes': anime_list})
    else:
        return render(request, 'recommend.html')'''


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

''' 
 url = 'https://graphql.anilist.co'
    query = #''
    query{
        media(type: ANIME, rank: {asc: view_count}, limit: 5,
        from: "2024-01-01", to: "2024-05-01") {
            title {
                romaji
                english
            }
            coverImage{
                large
            }
            viewCount
        }
    }
    #''
    response = requests.post(url, json={'query': query})
    data = response.json()
    anime_list = []

    for anime in data['data']['media']:
        title = anime["title"]["romaji"]
        image_url = anime["coverImage"]["large"]
        count = anime["viewCount"]

        anime_list.append({
            "images_jpg": image_url,
            "title": title,
            "count": count
        })
    return render(request, 'recommend.html', {'animes': anime_list})'''

