import requests

def get_anime_by_genre(genre):
    url = "https://api.jikan.moe/v4/anime"
    params = {"genre": genre}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        filtered_data = [item for item in data['data'] if item['genre']['name'] == 'genre']


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

        return data
    else:
        return None
