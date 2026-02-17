from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify

class Videogames(models.Model):
    uploaded_by = models.CharField(max_length=100)
    favorite_video_game = models.CharField(max_length=200)
    level_of_difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    fighting_a_feature = models.BooleanField(default=False)
    slug = models.SlugField(default='', null=False, db_index=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.favorite_video_game)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("videogame_detail", args=[self.slug])

    def __str__(self):
        return f"{self.uploaded_by}, their favorite video game is {self.favorite_video_game} the Difficulty level out of 10 is: {self.level_of_difficulty}, and is Fighting a feature? {self.fighting_a_feature}"
