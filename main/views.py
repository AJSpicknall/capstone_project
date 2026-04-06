from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import FeedbackForm
from .models import Feedback, Videogames


def get_favorites(request):
    """This will return the previously selected favorites to redisplay again."""
    return request.session.get("favorites", [])


def landing_page_view(request):
    """This will show all of the videogame submissions and they are ordered by difficulty and title."""
    videogames = Videogames.objects.order_by("level_of_difficulty", "favorite_video_game")
    return render(request, "main/base.html", {"videogames": videogames})


def about_view(request):
    """This one renders the about page."""
    return render(request, "main/about.html")


def videogame_detail(request, slug):
    """This one renders the details for a single videogame entry."""
    videogame = get_object_or_404(Videogames, slug=slug)
    return render(
        request,
        "main/detail.html",
        {
            "name": videogame.uploaded_by,
            "name_of_game": videogame.favorite_video_game,
            "difficulty": videogame.level_of_difficulty,
            "fight": videogame.fighting_a_feature,
        },
    )


@require_http_methods(["GET", "POST"])
def feedback_view(request):
    """This will display and process the feedback-submission form and any file uploads."""
    form = FeedbackForm(request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("feedback_success")

    return render(request, "main/feedback_form.html", {"form": form})


def feedback_success_view(request):
    """This one will render the feedback-confirmation page after a successful submission."""
    return render(request, "main/feedback_success.html")


def feedback_list_view(request):
    """This will show all of the feedback entries and then indicate which ones are favorited."""
    feedback_list = Feedback.objects.order_by("-id")
    favorites = get_favorites(request)
    return render(
        request,
        "main/feedback_list.html",
        {"feedback_list": feedback_list, "favorites": favorites},
    )


def feedback_detail_view(request, feedback_id):
    """This one is used to show a single feedback entry, and if it is a favorite post."""
    feedback = get_object_or_404(Feedback, id=feedback_id)
    favorites = get_favorites(request)
    is_favorite = feedback.id in favorites
    return render(
        request,
        "main/feedback_detail.html",
        {"feedback": feedback, "is_favorite": is_favorite},
    )

# Code adapted with assistance from ChatGPT (March 2026).

# Prompt: "I need an idea on how to make a class that will allow me to select favorite gallery options."

# Student review: I have learned how to make this class function with some assistance an now I understand better how to make favorite posts.

def toggle_favorite_view(request, feedback_id):
    """This will add or remove a feedback item from the sessions favorites list."""
    favorites = get_favorites(request)

    if feedback_id in favorites:
        favorites.remove(feedback_id)
    else:
        favorites.append(feedback_id)

    request.session["favorites"] = favorites

    # Code adapted with assistance from ChatGPT (April 2026).

    # Prompt: "How long should I set the code to stay til it expires?"

    # Student review: I just wanted a time that AI would recommend me put

    next_url = request.GET.get("next")
    if next_url:
        return redirect(next_url)

    return redirect("feedback_detail", feedback_id=feedback_id)
