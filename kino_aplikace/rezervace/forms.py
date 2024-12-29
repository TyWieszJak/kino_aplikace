from django import forms
from .models import Reservation, Movie, Seat


class ReservationForm(forms.ModelForm):
    seat = forms.ModelChoiceField(queryset=Seat.objects.filter(is_reserved=False), empty_label="Vyberte místo", widget=forms.Select())
    class Meta:
        model = Reservation
        fields = ['name', 'movie', 'number_of_seats']

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genre', 'length']