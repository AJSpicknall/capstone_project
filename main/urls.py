from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page_view, name="home"),
    path("about/", views.about_view, name="about"),
    path("<slug:slug>", views.videogame_detail, name="videogame_detail"),
]
