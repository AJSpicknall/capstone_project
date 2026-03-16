from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from .forms import FeedbackForm
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

# Code adapted with assistance from ChatGPT (February 2026).

# Prompt: "I am trying to get this new feedback_view function to run, what is going on with it?"

# Student review: I asked AI to help me fix what I was struggling with and help me debug the issue at hand, which was why it wasn't successfully going to my success page. But it adjusted what I put and got it to work out in the end. Yippee!

def feedback_view(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/feedback/success/")
    else:
        form = FeedbackForm()

    return render(request, "main/feedback_form.html", {
        "form": form,
    })


def feedback_success_view(request: HttpRequest) -> HttpResponse:
    return render(request, "main/feedback_success.html")
