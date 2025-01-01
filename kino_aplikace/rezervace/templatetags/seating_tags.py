from django import template
from rezervace.models import Seat
register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)
"""


@register.filter
def get_seat(seats, row_column):
    try:
        row, column = row_column.split(":")
        seat = seats.filter(row=row, seat_column=column).first()
        return seat if seat else f"Not found: {row}:{column}"
    except ValueError:
        return "Invalid format"

def get_seat(seats, row_column):
    try:
        row, column = row_column.split(":")
        # Pokud potřebujete vrátit konkrétní sedadlo
        return seats.filter(row=row, seat_column=column)  # nebo jiné logiky podle potřeby
    except ValueError:
        return None
"""