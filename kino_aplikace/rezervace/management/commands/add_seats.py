from django.core.management.base import BaseCommand
from rezervace.models import Movie, Seat

class Command(BaseCommand):
    help = "Přidá testovací místa a filmy do databáze"

    def handle(self, *args, **kwargs):
        movie, created = Movie.objects.get_or_create(
            title="Lords of the rings",
            defaults={"length": 180}
        )
        for row in ['A', 'B', 'C']:
            for column in range(1, 6):
                Seat.objects.get_or_create(row=row, seat_column=column, movie=movie)
        self.stdout.write(self.style.SUCCESS("Testovací místa a film byla úspěšně přidána."))
