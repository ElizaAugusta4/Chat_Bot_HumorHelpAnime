import random
import requests
from django.shortcuts import render, redirect
from .models import Anime, Genero
from .forms import UserPreference
from django.http import HttpResponse
from django.db.models import Count
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def recomendar_animes(user_preference):
    # Obtém os gêneros pesquisados pelo usuário e conta suas ocorrências
    generos_usuario = user_preference.values_list('genre', flat=True)
    generos_contagem = user_preference.values('genre').annotate(count=Count('genre'))

    # Convertendo os resultados em um dicionário
    generos_contagem_dict = {item['genre']: item['count'] for item in generos_contagem}

    # Obtém os animes que têm pelo menos um gênero pesquisado pelo usuário
    animes_relevantes = Anime.objects.filter(generos__nome__in=generos_usuario).distinct()

    # Calcula os vetores de frequência dos gêneros dos animes
    vetores_animes = []
    for anime in animes_relevantes:

        vetor_anime = [anime.generos.filter(nome=genero).count()
                       for genero in generos_usuario]
        vetores_animes.append(vetor_anime)

    print(vetores_animes)

    # Normaliza os vetores de frequência
    vetores_animes_norm = np.array(vetores_animes) / np.linalg.norm(vetores_animes, axis=1)[:, np.newaxis]
    vetor_usuario_norm = np.array([generos_contagem_dict.get(genero, 0) for genero in generos_usuario]) / sum(generos_contagem_dict.values())

    # Calcula a similaridade de cosseno entre o vetor do usuário e os vetores dos animes
    similaridades = cosine_similarity([vetor_usuario_norm], vetores_animes_norm)

    # Associa cada anime com sua pontuação de similaridade
    animes_similaridade = list(zip(animes_relevantes, similaridades[0]))

    # Classifica os animes com base na pontuação de similaridade
    animes_similaridade.sort(key=lambda x: x[1], reverse=True)

    # Retorna os animes recomendados
    print([anime for anime, _ in animes_similaridade])
    return [anime for anime, _ in animes_similaridade]


def base(request):
    user = UserPreference.objects.all()
    recomendar_animes(user)
    url = 'https://graphql.anilist.co'
    query = """
           query {
              Page(page:1,perPage:1000){ 
                   media(type:ANIME) {
                       title {
                           romaji
                           english
                       }
                       genres
                       description
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
        sinopse = anime["description"]
        image_url = anime["coverImage"]["large"]

        anime_list.append({
            "images_jpg": image_url,
            "title": title,
            "sinopse": sinopse,
            "genres": genres
        })
        for anime_data in anime_list:
            # Verifique se o anime já existe no banco de dados com o mesmo título
            existing_anime = Anime.objects.filter(title=anime_data['title']).first()

            # Se o anime já existir, pule para o próximo anime na lista
            if existing_anime:
                continue

            # Verifique se todos os gêneros existem e obtenha os objetos Genero correspondentes
            generos = []
            for genre_name in anime_data['genres']:
                genero, created = Genero.objects.get_or_create(nome=genre_name)
                generos.append(genero)

            # Crie o objeto Anime
            anime = Anime.objects.create(
                title=anime_data['title'],
                sinopse=anime_data['sinopse'],
                popularidade=0
            )

            # Adicione os gêneros ao anime
            anime.generos.add(*generos)

            # Salve o anime
            anime.save()

    # Selecione aleatoriamente 10 animes da lista
    random_animes = random.sample(anime_list, 24)

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
                       description
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
        sinopse = anime['description']
        image_url = anime["coverImage"]["large"]

        anime_list.append({
            "images_jpg": image_url,
            "title": title,
            "genres": genres,
            "sinopse": sinopse,
            "popularity": popularity
        })

    # Ordenar a lista de animes por popularidade em ordem decrescente
    anime_list.sort(key=lambda x: x['popularity'], reverse=True)

    return render(request, 'index.html', {'animes_random': random_animes, 'animes_top': anime_list[:5]})


def get_anime_by_genre(request):
    if request.method == 'POST':
        genre = request.POST.get('genre')
        user_preference = UserPreference()
        user_preference.genre = genre
        user_preference.save()
        url = 'https://graphql.anilist.co'
        query = """
            query($genre: String) {
               Page(page:1,perPage:1000){ 
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

        turn_animes = random.sample(anime_list, 24)

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
                               description
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
            sinopse = anime['description']
            image_url = anime["coverImage"]["large"]

            anime_list.append({
                "images_jpg": image_url,
                "title": title,
                "genres": genres,
                "sinopse": sinopse,
                "popularity": popularity
            })

        # Ordenar a lista de animes por popularidade em ordem decrescente
        anime_list.sort(key=lambda x: x['popularity'], reverse=True)

        return render(request, 'search.html', {'animes': turn_animes, 'animes_top': anime_list[:5]})
    else:
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
                       description
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
            sinopse = anime['description']
            image_url = anime["coverImage"]["large"]

            anime_list.append({
                "images_jpg": image_url,
                "title": title,
                "genres": genres,
                "sinopse": sinopse,
                "popularity": popularity
            })

        # Ordenar a lista de animes por popularidade em ordem decrescente
        anime_list.sort(key=lambda x: x['popularity'], reverse=True)

        return render(request, 'search.html', {'animes_top': anime_list[:5]})
