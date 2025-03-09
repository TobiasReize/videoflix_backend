from django.core.management.base import BaseCommand
from videoflix_app.admin import VideoResource
import datetime


class Command(BaseCommand):
    help = "Exportiert alle Videos als JSON und speichert sie als Backup."

    def handle(self, *args, **kwargs):
        dataset = VideoResource().export()
        json_data = dataset.json

        # Erstelle einen Dateinamen mit Zeitstempel
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"videos_backup_{timestamp}.json"

        # Schreibe den JSON-String in die Datei
        with open(filename, "w") as f:
            f.write(json_data)

        self.stdout.write(self.style.SUCCESS(f"Backup gespeichert als {filename}"))
