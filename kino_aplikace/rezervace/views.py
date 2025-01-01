from django.http import HttpResponse
import logging
from .forms import MovieForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Movie, Reservation, Seat
from string import ascii_uppercase
from django.contrib import messages


def index(request):
    movies = (Movie.objects.all())  # Získání všech filmů z databáze
    return render(request, 'reservation/index.html', {'movies': movies})


def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            # Získání vybraného sedadla
            seat_id = request.POST.get("seat_id")
            seat = get_object_or_404(Seat, id=seat_id)

            # Získání filmu (měl by být součástí URL nebo session)
            movie_id = request.POST.get("movie_id")  # Předpokládáme, že movie_id je v POST datech
            movie = get_object_or_404(Movie, id=movie_id)

            reservation = form.save(commit=False)
            reservation.seat = seat
            reservation.movie = movie
            reservation.save()

            # Nastavení sedadla na rezervováno
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


def generate_seat_map(seats):
    # Předpokládejme, že sedadla mají vlastnosti 'row' a 'column'
    # (pokud ne, můžete si upravit podle toho, jak máte definováno)

    seat_map = {}

    for seat in seats:
        # Vytvoří klíč pro každé sedadlo kombinací řady a sloupce
        # Například 'A1', 'B2', 'C3' atd.
        seat_key = f"{seat.row}{seat.column}"
        seat_map[seat_key] = seat  # Přiřazení sedadla do mapy

    return seat_map

def movie_seats(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    seats = Seat.objects.filter(movie=movie)
    rows = ['A', 'B', 'C','D',"E","F","G","H","J"]  # Příklad řad
    columns = range(1, 11)  # Příklad sloupců (1-10)
    seat_map = generate_seat_map(seats)
    # Mapování sedadel podle řady a sloupce


    #print(seat_map)  # Debug výstup, který ukáže obsah seat_map

    return render(request, 'reservation/movie_seats.html', {
        'movie': movie,
        'seat_map': seat_map,
        'rows': rows,
        'columns': columns,
    })

def success(request):
    return render(request, 'reservation/success.html')


def reserve_seat(request, movie_id, seat_id):
    movie = get_object_or_404(Movie, id=movie_id)
    seat = get_object_or_404(Seat, id=seat_id)


    # Pokud je sedadlo již rezervováno, přesměruj na jinou stránku nebo zobraz chybovou hlášku.
    if seat.is_reserved:
        return redirect('movie_seats', movie_id=movie.id)  # Příklad přesměrování na stránku s plánem sedadel

    # Pokud ještě není rezervováno, rezervuj sedadlo
    seat.is_reserved = True
    seat.save()

    # Vytvoření rezervace (pokud je potřeba)
    if request.method == "POST":
        reservation_form = ReservationForm(request.POST)
        if reservation_form.is_valid():
            reservation = reservation_form.save(commit=False)
            reservation.movie = movie
            reservation.seat = seat
            reservation.save()
            return redirect('success')  # Přesměrování na stránku s potvrzením úspěchu
    else:
        reservation_form = ReservationForm()

    return render(request, 'reservation/movie_seats.html', {'movie': movie, 'seat': seat, 'reservation_form': reservation_form})



