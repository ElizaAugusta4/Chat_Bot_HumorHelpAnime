from anime_recommender.recommendations.models import Anime

# Obtenha todos os títulos únicos dos animes no banco de dados
unique_titles = Anime.objects.values_list('title', flat=True).distinct()

# Itere sobre os títulos únicos
for title in unique_titles:
    # Obtenha todos os registros de anime com o mesmo título
    anime_duplicates = Anime.objects.filter(title=title)[1:]

    # Exclua os registros duplicados
    for duplicate in anime_duplicates:
        duplicate.delete()