from django.contrib import admin

from .models import Genre, Publisher, VideogameProfile, Videogames


class VideogamesAdmin(admin.ModelAdmin):
    list_display = (
        "favorite_video_game",
        "uploaded_by",
        "publisher",
        "level_of_difficulty",
        "fighting_a_feature",
        "slug",
    )
    list_filter = ("fighting_a_feature", "publisher", "genres", "level_of_difficulty")
    search_fields = ("favorite_video_game", "uploaded_by", "publisher__name", "genres__name")


class PublisherAdmin(admin.ModelAdmin):
    list_display = ("name", "headquarters")
    search_fields = ("name", "headquarters")


class GenreAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


class VideogameProfileAdmin(admin.ModelAdmin):
    list_display = ("videogame", "release_year")
    search_fields = ("videogame__favorite_video_game", "videogame__uploaded_by")


admin.site.register(Videogames, VideogamesAdmin)
admin.site.register(Publisher, PublisherAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(VideogameProfile, VideogameProfileAdmin)
