from pathlib import Path

from django.conf import settings
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.text import slugify
from django.views import View
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import FeedbackForm
from .models import Feedback, Videogames


def resolve_feedback_headshot_url(user_name):
    base_name = slugify(user_name)
    for extension in ("png", "jpg", "jpeg", "webp"):
        relative_path = Path("feedback_headshots") / f"{base_name}.{extension}"
        absolute_path = Path(settings.MEDIA_ROOT) / relative_path
        if absolute_path.exists():
            return f"{settings.MEDIA_URL.rstrip('/')}/{relative_path.as_posix()}"
    return None


class GameImageMixin:
    """Resolve a static image path for each game based on title/slug."""

    image_file_by_slug = {
        "minecraft": "minecraft.png",
        "terraria": "terraria.png",
        "goldeneye-007": "007.png",
        "cooking-mama": "cooking_mama.png",
        "celeste": "celeste.png",
        "metroid": "metroid.png",
        "metroid-prime": "metroid.png",
        "final-fantasy-vii": "final_fantasy.png",
        "stardew-valley": "stardew_valley.png",
        "the-legend-of-zelda-a-link-to-the-past": "legend_of_zelda.png",
        "super-mario-64": "Super_Mario_64.png",
        "elden-ring": "elden_ring.png",
        "portal-2": "portal_2.png",
        "hollow-knight": "hollow_knight.png",
        "monster-hunter-world": "monster_hunter_world.png",
        "mass-effect-2": "mass_effect_2.png",
        "the-witcher-3-wild-hunt": "witcher_3.png",
        "overwatch-2": "overwatch_2.png",
        "street-fighter-6": "street_fighter_6.png",
        "baldurs-gate-3": "baldurs_gate_3.png",
        "forza-horizon-5": "forza_5.png",
        "tetris-effect-connected": "tetris.png",
        "apex-legends": "apex.png",
        "god-of-war-ragnarok": "god_of_war_ragnarok.png",
        "resident-evil-4": "resident_evil_4.png",
        "persona-5-royal": "persona_5.png",
        "red-dead-redemption-2": "red_dead_redemption.png",
        "diablo-iv": "diable_4.png",
        "animal-crossing-new-horizons": "animal_crossing.png",
        "animal-crossing": "animal_crossing.png",
    }

    def assign_game_image(self, game):
        image_name = self.image_file_by_slug.get(game.slug)
        if image_name:
            game.image_static_path = f"main/images/Games/{image_name}"
        else:
            game.image_static_path = "main/images/aj-image.jpeg"
        return game


class FavoritesSessionMixin:
    """Provide reusable session helpers for reading/writing favorite feedback IDs."""

    session_key = "favorites"

    def get_favorites(self):
        raw_values = self.request.session.get(self.session_key, [])
        return [value for value in raw_values if isinstance(value, int)]

    def set_favorites(self, favorites):
        self.request.session[self.session_key] = favorites
        self.request.session.modified = True


class LandingPageView(GameImageMixin, ListView):
    """Render the home page with all games, ordered and annotated with image paths."""

    model = Videogames
    template_name = "main/home.html"
    context_object_name = "videogames"
    ordering = ("level_of_difficulty", "favorite_video_game")

    def get_queryset(self):
        queryset = super().get_queryset()
        return [self.assign_game_image(game) for game in queryset]


class AboutView(TemplateView):
    """Render the static About page describing the project."""

    template_name = "main/about.html"


class VideogameDetailView(GameImageMixin, DetailView):
    """Show one game by slug and attach its static image path for template rendering."""

    model = Videogames
    template_name = "main/detail.html"
    context_object_name = "videogame"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["videogame"] = self.assign_game_image(self.object)
        return context


class FeedbackCreateView(CreateView):
    """Display and process the feedback form, then redirect to a success page."""

    model = Feedback
    form_class = FeedbackForm
    template_name = "main/feedback_form.html"
    success_url = reverse_lazy("feedback_success")

    def form_valid(self, form):
        messages.success(self.request, "Feedback submitted successfully.")
        return super().form_valid(form)


class FeedbackSuccessView(TemplateView):
    """Render the confirmation page after feedback submission."""

    template_name = "main/feedback_success.html"


class FeedbackListView(FavoritesSessionMixin, ListView):
    """List all feedback posts and expose session favorites for gallery badges/actions."""

    model = Feedback
    template_name = "main/feedback_list.html"
    context_object_name = "feedback_list"
    ordering = ("-id",)

    def get_queryset(self):
        queryset = list(super().get_queryset())
        for feedback in queryset:
            feedback.headshot_url = resolve_feedback_headshot_url(feedback.user_name)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["favorites"] = self.get_favorites()
        return context


class FeedbackDetailView(FavoritesSessionMixin, DetailView):
    """Show one feedback entry and indicate whether it is currently favorited in session."""

    model = Feedback
    template_name = "main/feedback_detail.html"
    context_object_name = "feedback"
    pk_url_kwarg = "feedback_id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_favorite"] = self.object.id in self.get_favorites()
        context["headshot_url"] = resolve_feedback_headshot_url(self.object.user_name)
        return context


class ToggleFavoriteView(FavoritesSessionMixin, View):
    """Handle POST requests that toggle a feedback ID in the session favorites list."""

    def post(self, request, feedback_id):
        favorites = self.get_favorites()
        feedback = Feedback.objects.filter(id=feedback_id).first()
        if feedback is None:
            messages.error(request, "Feedback entry was not found.")
            return redirect("feedback_list")

        if feedback_id in favorites:
            favorites.remove(feedback_id)
            messages.info(request, "Removed from favorites.")
        else:
            favorites.append(feedback_id)
            messages.success(request, "Added to favorites.")

        self.set_favorites(favorites)

        next_url = request.POST.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect(reverse("feedback_detail", kwargs={"feedback_id": feedback_id}))
