from django import forms
from django.core.exceptions import ValidationError

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ["user_name", "email", "subject", "message", "image"]
        labels = {
            "user_name": "Your Name",
            "email": "Your Email",
            "subject": "Subject",
            "message": "Message",
            "image": "Upload Image",
        }
        widgets = {
            "message": forms.Textarea(attrs={"rows": 4}),
        }

# Code adapted with assistance from ChatGPT (April 2026).

# Prompt: "I want a better understanding on What I should put that would make entries to my form be cleaner."

# Student review: I got a better understanding on how to create checkers for each input type that I am using.


    def clean_message(self):
        """This one will reject any messages that have only whitespace."""
        message = self.cleaned_data.get("message", "")
        if not message.strip():
            raise ValidationError("Please enter a message before submitting.")
        return message

    def clean_image(self):
        """This will make sure the right image format gets uploaded to my form."""
        image = self.cleaned_data.get("image")
        if not image:
            return image

        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if image.content_type not in allowed_types:
            raise ValidationError("Please upload a JPG, PNG, GIF, or WEBP image.")

        return image
