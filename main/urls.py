from django.urls import path
from . import views

urlpatterns = [
    path("", views.LandingPageView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("feedback/", views.FeedbackCreateView.as_view(), name="feedback"),
    path("feedback/success/", views.FeedbackSuccessView.as_view(), name="feedback_success"),
    path("feedback/submissions/", views.FeedbackListView.as_view(), name="feedback_list"),
    path("feedback/submissions/<int:feedback_id>/", views.FeedbackDetailView.as_view(), name="feedback_detail"),
    path("feedback/submissions/<int:feedback_id>/favorite/", views.ToggleFavoriteView.as_view(), name="toggle_favorite"),
    path("<slug:slug>/", views.VideogameDetailView.as_view(), name="videogame_detail"),
]
