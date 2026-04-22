from django import forms
from django.core.exceptions import ValidationError

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    max_image_size_bytes = 5 * 1024 * 1024

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
            "user_name": forms.TextInput(attrs={"placeholder": "Name visible to other visitors"}),
            "email": forms.EmailInput(attrs={"placeholder": "name@example.com"}),
            "subject": forms.TextInput(attrs={"placeholder": "What is this feedback about?"}),
            "message": forms.Textarea(attrs={"rows": 4}),
        }

    def clean_user_name(self):
        user_name = self.cleaned_data.get("user_name", "").strip()
        if len(user_name) < 2:
            raise ValidationError("Please enter at least 2 characters for your name.")
        return user_name

    def clean_subject(self):
        subject = self.cleaned_data.get("subject", "").strip()
        if len(subject) < 5:
            raise ValidationError("Subject must be at least 5 characters long.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get("message", "")
        if not message.strip():
            raise ValidationError("Please enter a message before submitting.")
        if len(message.strip()) < 15:
            raise ValidationError("Message should be at least 15 characters long.")
        return message.strip()

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if not image:
            return image

        allowed_types = {"image/jpeg", "image/png", "image/gif", "image/webp"}
        if image.content_type not in allowed_types:
            raise ValidationError("Please upload a JPG, PNG, GIF, or WEBP image.")
        if image.size > self.max_image_size_bytes:
            raise ValidationError("Image must be 5 MB or smaller.")

        return image
