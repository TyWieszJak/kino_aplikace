from django.shortcuts import render, redirect
from .forms import ReservationForm
from.models import Movie


def index(request):
    movies = (Movie.objects.all())  # Získání všech filmů z databáze
    return render(request, 'reservation/index.html', {'movies': movies})


def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = ReservationForm()

    return render(request, 'reservation/reservation.html', {'form': form})