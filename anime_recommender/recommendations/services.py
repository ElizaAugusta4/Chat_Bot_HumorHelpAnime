import requests

def get_anime_by_genre(genre):
    url = "https://api.jikan.moe/v4/anime"
    params = {"genre": genre}
    response = requests.get(url, params=params)
    print(response.status_code) 
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        return None
