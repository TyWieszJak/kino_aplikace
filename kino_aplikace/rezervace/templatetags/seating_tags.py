from django import template
from rezervace.models import Seat

register = template.Library()

@register.filter
def get_seat(seats, row_column):
    try:
        row, column = row_column.split(":")
        # Pokud potřebujete vrátit konkrétní sedadlo
        return seats.filter(row=row, seat_column=column).first()  # nebo jiné logiky podle potřeby
    except ValueError:
        return None
