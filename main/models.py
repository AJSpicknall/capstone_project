from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

class Publisher(models.Model):
    name = models.CharField(max_length=150)
    headquarters = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class Videogames(models.Model):
    uploaded_by = models.CharField(max_length=100)
    favorite_video_game = models.CharField(max_length=200)
    level_of_difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    fighting_a_feature = models.BooleanField(default=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True, related_name="videogames")
    slug = models.SlugField(default="", null=False, db_index=True, unique=True)

    def save(self, *args, **kwargs):
        base_slug = slugify(self.favorite_video_game) or "videogame"
        slug = base_slug
        suffix = 1
        while (
            Videogames.objects.filter(slug=slug)
            .exclude(pk=self.pk)
            .exists()
        ):
            slug = f"{base_slug}-{suffix}"
            suffix += 1
        self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("videogame_detail", args=[self.slug])

    def __str__(self):
        return f"{self.uploaded_by}, their favorite video game is {self.favorite_video_game} the Difficulty level out of 10 is: {self.level_of_difficulty}, and is Fighting a feature? {self.fighting_a_feature}"


class VideogameProfile(models.Model):
    videogame = models.OneToOneField(Videogames, on_delete=models.CASCADE, related_name="profile")
    release_year = models.PositiveIntegerField(null=True, blank=True)
    platform_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Profile for {self.videogame.favorite_video_game}"


class Feedback(models.Model):
    user_name = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=50)
    message = models.TextField()
    image = models.ImageField(upload_to="feedback_uploads/", blank=True, null=True)

    def get_absolute_url(self):
        return reverse("feedback_detail", args=[self.id])

    def get_favorite_toggle_url(self):
        return reverse("toggle_favorite", args=[self.id])

    def __str__(self):
        return f"{self.user_name}: {self.subject}"
