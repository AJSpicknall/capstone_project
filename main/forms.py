from django import forms

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
