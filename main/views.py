from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Videogames

def landing_page_view(request: HttpRequest) -> HttpResponse:
    videogames = Videogames.objects.all().order_by("level_of_difficulty", "favorite_video_game")
    return render(request, "main/base.html", {"videogames": videogames})

def about_view(request: HttpRequest) -> HttpResponse:
    return render(request, "main/about.html")

def videogame_detail(request, slug):
    try:
        videogame = Videogames.objects.get(slug=slug)
    except:
        raise get_object_or_404()
    
    return render(request, 'main/detail.html', {
        'name': videogame.uploaded_by,
        'name_of_game': videogame.favorite_video_game,
        'difficulty': videogame.level_of_difficulty,
        'fight': videogame.fighting_a_feature,
    })
