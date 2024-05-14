from django.shortcuts import render
from .services import get_anime_by_genre

def recommend(request):
    if request.method == 'POST':
        genre = request.POST['genre']
        animes = get_anime_by_genre(genre)
        return render(request, 'recommend.html', {'animes': animes})
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