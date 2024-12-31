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


def movie_seats(request, movie_id):
    # Získání filmu podle ID
    movie = get_object_or_404(Movie, id=movie_id)
    # Získání všech sedadel pro tento film
    seats = movie.seats.all()
    # Definování řad (A až J)
    rows = list(ascii_uppercase[:10])  # A až J
    # Definování sloupců (1 až 10)
    columns = list(range(1, 11))  # 1 až 10

    # Předání dat do šablony
    return render(request, 'reservation/movie_seats.html', {
        'movie': movie,
        'seats': seats,
        'rows': rows,
        'columns': columns
    })

def success(request):
    return render(request, 'reservation/success.html')


def reserve_seat(request, movie_id, seat_id):
    movie = Movie.objects.get(id=movie_id)
    seat = Seat.objects.get(id=seat_id)

    if seat.is_reserved:
        messages.error(request, f"Sedadlo {seat.row}{seat.seat_column} je již obsazeno.")
        return redirect('movie_seats', movie_id=movie.id)  # Přesměrování na plánek sedadel

    if request.method == 'POST':
        # Aktualizace stavu sedadla na obsazené
        seat.is_reserved = True
        seat.save()

        # Případně vytvoření záznamu o rezervaci (pokud máte model rezervace)
        # Reservation.objects.create(name=request.POST['name'], seat=seat, movie=movie)

        messages.success(request, f"Sedadlo {seat.row}{seat.seat_column} bylo úspěšně rezervováno.")
        return redirect('movie_seats', movie_id=movie.id)

    return render(request, 'reservation/reserve_seat.html', {
        'movie': movie,
        'seat': seat,
    })
