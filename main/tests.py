from django.test import TestCase
from django.urls import reverse

from .forms import FeedbackForm
from .models import Feedback, Videogames


class FeedbackFormTests(TestCase):
    def test_message_cannot_be_only_whitespace(self):
        form = FeedbackForm(
            data={
                "user_name": "AJ",
                "email": "aj@gmail.com",
                "subject": "Feedback topic",
                "message": "   ",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("message", form.errors)


class FavoriteSessionTests(TestCase):
    def setUp(self):
        self.feedback = Feedback.objects.create(
            user_name="Casey",
            email="casey@gmail.com",
            subject="Navigation suggestion",
            message="The menu works well but could use stronger mobile spacing.",
        )

    def test_toggle_favorite_adds_entry(self):
        response = self.client.post(
            reverse("toggle_favorite", args=[self.feedback.id]),
            data={"next": reverse("feedback_list")},
        )
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.feedback.id, self.client.session.get("favorites", []))


class LandingPageViewTests(TestCase):
    def test_home_page_renders_games(self):
        Videogames.objects.create(
            uploaded_by="Alex",
            favorite_video_game="Portal 2",
            level_of_difficulty=3,
            fighting_a_feature=False,
        )
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Portal 2")
