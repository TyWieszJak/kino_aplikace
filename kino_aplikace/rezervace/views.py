from .forms import MovieForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Movie, Reservation, Seat


def index(request):
    movies = (Movie.objects.all())  # Získání všech filmů z databáze
    return render(request, 'reservation/index.html', {'movies': movies})


def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            seat = form.cleaned_data["seat"]
            seat.is_reserved = True
            seat.save()
            return redirect('success')
    else:
        form = ReservationForm()

    return render(request, 'reservation/reservation.html', {'form': form})


def all_reservation(request):
    reservations = (Reservation.objects.all())
    return render(request, 'reservation/all_reservation.html', {'reservations': reservations})

def add_film(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = MovieForm()

    return render(request, 'reservation/add_film.html', {'form': form})
def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie.delete()
    return redirect('index')


def movie_seats(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    seats = movie.seats.all()
    return render(request, 'reservation/movie_seats.html', {'movie': movie, 'seats': seats})


def success(request):
    return render(request, 'reservation/success.html')