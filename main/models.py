from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Videogames(models.Model):
    uploaded_by = models.CharField(max_length=100)
    favorite_video_game = models.CharField(max_length=200)
    level_of_difficulty = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    fighting_a_feature = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.uploaded_by}, their favorite video game is {self.favorite_video_game} the Difficulty level out of 10 is: {self.level_of_difficulty}, and is Fighting a feature? {self.fighting_a_feature}"
