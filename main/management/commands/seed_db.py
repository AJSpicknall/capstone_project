import csv
from django.core.management.base import BaseCommand
from main.models import Videogames

class Command(BaseCommand):
    help = "Imports videogame data from a CSV file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to the csv file")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        created_count = 0
        updated_count = 0

        try:
            with open(file_path, mode="r", encoding="utf-8", newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    fighting_a_feature_bool = (
                        str(row["fighting_a_feature"]).strip().lower() == "true"
                    )

                    videogame, created = Videogames.objects.get_or_create(
                        uploaded_by=row["uploaded_by"].strip(),
                        favorite_video_game=row["favorite_video_game"].strip(),
                        defaults={
                            "level_of_difficulty": int(row["level_of_difficulty"]),
                            "fighting_a_feature": fighting_a_feature_bool,
                        },
                    )

                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f"Imported: {row['favorite_video_game']}"
                            )
                        )
                    else:
                        videogame.level_of_difficulty = int(row["level_of_difficulty"])
                        videogame.fighting_a_feature = fighting_a_feature_bool
                        videogame.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.WARNING(
                                f"Updated: {row['favorite_video_game']}"
                            )
                        )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Done. Created: {created_count}, Updated: {updated_count}"
                    )
                )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
