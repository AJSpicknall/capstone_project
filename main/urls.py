from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("feedback/", views.feedback_view, name="feedback"),
    path("feedback/success/", views.feedback_success_view, name="feedback_success"),
    path("feedback/submissions/", views.feedback_list_view, name="feedback_list"),
    path("feedback/submissions/<int:feedback_id>/", views.feedback_detail_view, name="feedback_detail"),
    path("feedback/submissions/<int:feedback_id>/favorite/", views.toggle_favorite_view, name="toggle_favorite"),
    path("<slug:slug>", views.videogame_detail, name="videogame_detail"),
]
