from django.shortcuts import render
from.services import get_anime_by_genre

def recommend(request):
    if request.method == 'POST':
        genre = request.POST['genre']
        animes = get_anime_by_genre(genre)
        return render(request, 'recommend.html', {'animes': animes})
    else:
        return render(request, 'recommend.html')
