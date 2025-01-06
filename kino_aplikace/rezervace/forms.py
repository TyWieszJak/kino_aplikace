from django import forms
from .models import Reservation, Movie, Seat


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['name' ]#'movie', 'seat', 'number_of_seats'

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'length']