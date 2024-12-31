from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Movie, Seat


@receiver(post_save, sender=Movie)
def create_seats(sender, instance, created, **kwargs):
    if created:
        rows = [chr(i) for i in range(ord('A'), ord('J') + 1)]
        for row in rows:
            for column_number in range(1,11):
                Seat.objects.create(
                    row=row,
                    seat_column=column_number,
                    seat_number=column_number,
                    movie=instance
                )
        print(f"Plan sedadel vytvořen pro film: {instance.title}")