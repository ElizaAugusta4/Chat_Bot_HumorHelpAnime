import requests

def get_anime_by_genre(genre):
    url = "https://api.jikan.moe/v4/animes"
    params = {"genre": genre}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None
