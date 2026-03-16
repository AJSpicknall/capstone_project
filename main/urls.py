from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("feedback/", views.feedback_view, name="feedback"),
    path("feedback/success/", views.feedback_success_view, name="feedback_success"),
    path("<slug:slug>", views.videogame_detail, name="videogame_detail"),
]
