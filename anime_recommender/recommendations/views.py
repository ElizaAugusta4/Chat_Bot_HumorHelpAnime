from django.shortcuts import render
from django.views import View
from .services import fetch_animes_by_genre


#Funcao para renderizar a tela inicial
def anime_view(request):
    return render(request, 'index.html')

#classe e métodos para recomendação de animes
class RecommendView(View):
    def get(self, request):
        stage = request.session['stage'] = None
        if stage is None or stage == 'greeting':
            message = 'Olá, tudo bem?'
            request.session['stage'] = 'response_greeting'
        elif stage == 'response_greeting':
            message = 'Qual gênero de animes você gosta?'
            request.session['stage'] = 'ask_genre'
        else:
            message = 'Desculpe, não entendi.'
        return render(request, 'recommend.html', {'message': message, 'stage': stage})

    def post(self, request):
        stage = request.session.get('stage', 'greeting')
        if stage == 'response_greeting':
            request.session['stage'] = 'ask_genre'
            return render(request, 'recommend.html', {'message': 'Qual gênero de animes você gosta?', 'stage': 'ask_genre'})
        elif stage == 'ask_genre':
            genre = request.POST['genre']
            animes = fetch_animes_by_genre(genre)
            return render(request, 'recommend.html', {'animes': animes, 'stage': 'recommend'})
        return render(request, 'recommend.html', {'message': 'Desculpe, não entendi.', 'stage': 'error'})
