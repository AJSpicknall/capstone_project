import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from main.models import Feedback, Genre, Publisher, VideogameProfile, Videogames


class Command(BaseCommand):
    help = "Import videogame data from CSV into game, publisher, genre, and profile models."

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path",
            nargs="?",
            default="data.csv",
            help="Path to CSV file (defaults to data.csv in project root).",
        )
        parser.add_argument(
            "--with-feedback",
            action="store_true",
            help="Seed additional feedback entries for gallery volume.",
        )

    def handle(self, *args, **kwargs):
        file_path = Path(kwargs["file_path"])
        if not file_path.exists():
            raise CommandError(f"CSV file not found: {file_path}")

        created_count = 0
        updated_count = 0

        with file_path.open(mode="r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)

            for row in reader:
                game_name = row.get("favorite_video_game", "").strip()
                uploader = row.get("uploaded_by", "").strip()
                if not game_name or not uploader:
                    self.stdout.write(self.style.WARNING("Skipping row with missing required values."))
                    continue

                fighting_a_feature = str(row.get("fighting_a_feature", "")).strip().lower() == "true"
                difficulty = int(row.get("level_of_difficulty", 1))

                publisher = self._resolve_publisher(row)

                videogame, created = Videogames.objects.update_or_create(
                    favorite_video_game=game_name,
                    defaults={
                        "uploaded_by": uploader,
                        "level_of_difficulty": difficulty,
                        "fighting_a_feature": fighting_a_feature,
                        "publisher": publisher,
                    },
                )

                if created:
                    created_count += 1
                else:
                    updated_count += 1

                self._set_genres(videogame, row.get("genres", ""))
                self._set_profile(videogame, row)

        feedback_created = 0
        if kwargs.get("with_feedback"):
            feedback_created = self._seed_feedback()

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Games created: {created_count}, games updated: {updated_count}, "
                f"feedback created: {feedback_created}"
            )
        )

    def _resolve_publisher(self, row):
        publisher_name = row.get("publisher", "").strip()
        if not publisher_name:
            return None
        headquarters = row.get("headquarters", "").strip() or "Unknown"
        publisher, _ = Publisher.objects.get_or_create(
            name=publisher_name,
            defaults={"headquarters": headquarters},
        )
        if publisher.headquarters == "Unknown" and headquarters != "Unknown":
            publisher.headquarters = headquarters
            publisher.save(update_fields=["headquarters"])
        return publisher

    def _set_genres(self, videogame, raw_genres):
        names = [name.strip() for name in raw_genres.split("|") if name.strip()]
        if not names:
            return
        genre_objects = []
        for name in names:
            genre, _ = Genre.objects.get_or_create(name=name)
            genre_objects.append(genre)
        videogame.genres.set(genre_objects)

    def _set_profile(self, videogame, row):
        release_year_value = row.get("release_year", "").strip()
        platform_notes = row.get("platform_notes", "").strip()
        if not release_year_value and not platform_notes:
            return

        release_year = int(release_year_value) if release_year_value.isdigit() else None
        profile, _ = VideogameProfile.objects.get_or_create(videogame=videogame)
        profile.release_year = release_year
        profile.platform_notes = platform_notes
        profile.save()

    def _seed_feedback(self):
        feedback_rows = [
            ("Jules", "jules@gmail.com", "The General Look", "The overall style of the website looks clean and easy to read."),
            ("Rory", "Rory1212@outlook.com", "The Overall Performance", "The timeliness of the pages loading time is wonderful and easy to work with."),
            ("Parker", "parkerlovingston@icloud.com", "It's Data Quality", "I do enjoy seeing the basic data that is displayed for users like me."),
            ("Noel", "niko@gmail.com", "The Forms Validation features", "This form to write a review is really easy to understand and submit."),
            ("Skye", "skye5890@icloud.com", "The color contrast is good", "I'm a big fan of colors and the contrast of this website is easy on the eyes."),
            ("Jordan", "jordanistheb3st@yahoo.com", "Simplicity of the Gallery Cards", "The cards make it easy to know which belongs to which and know what data belong to what."),
        ]

        created = 0
        for user_name, email, subject, message in feedback_rows:
            _, is_created = Feedback.objects.update_or_create(
                user_name=user_name,
                defaults={
                    "email": email,
                    "subject": subject,
                    "message": message,
                },
            )
            if is_created:
                created += 1
        return created
