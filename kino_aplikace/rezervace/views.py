from django.http import HttpResponse
import logging
from .forms import MovieForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ReservationForm
from .models import Movie, Reservation, Seat
from string import ascii_uppercase
from django.contrib import messages


def index(request):
    movies = (Movie.objects.all())
    return render(request, 'reservation/index.html', {'movies': movies})


def reservation(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            seat_id = request.POST.get("seat_id")
            seat = get_object_or_404(Seat, id=seat_id)
            movie_id = request.POST.get("movie_id")
            movie = get_object_or_404(Movie, id=movie_id)

            reservation = form.save(commit=False)
            reservation.seat = seat
            reservation.movie = movie
            reservation.save()
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
    movie = get_object_or_404(Movie, id=movie_id)
    seats = movie.seats.all()
    rows = list(ascii_uppercase[:10])  # A až J
    columns = list(range(1, 11))  # 1 až 10


    seat_map = [[None for _ in columns] for _ in rows]
    for seat in seats:
        row_index = rows.index(seat.row)
        column_index = columns.index(seat.seat_column)
        seat_map[row_index][column_index] = seat


    return render(request, 'reservation/movie_seats.html', {
        'movie': movie,
        'seat_map': seat_map,
        'rows': rows,
        'columns': columns
    })

def success(request):
    return render(request, 'reservation/success.html')


def reserve_seat(request, movie_id, seat_id):

    movie = get_object_or_404(Movie, id=movie_id)
    seat = get_object_or_404(Seat, id=seat_id)

    if seat.is_reserved:
        return redirect('movie_seats', movie_id=movie.id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():

            reservation = form.save(commit=False)
            reservation.movie = movie
            reservation.seat = seat
            reservation.number_of_seats = 1
            reservation.save()


            seat.is_reserved = True
            seat.save()

            return redirect('movie_seats', movie_id=movie.id)

    else:
        form = ReservationForm()


    rows = list(ascii_uppercase[:10])  # A-J řady
    columns = list(range(1, 11))  # Sloupce 1-10


    seat_map = [[None for _ in columns] for _ in rows]
    seats = movie.seats.all()
    for seat in seats:
        row_index = rows.index(seat.row)
        column_index = columns.index(seat.seat_column)
        seat_map[row_index][column_index] = seat

    return render(request, 'reservation/reserve_seat.html', {
        'movie': movie,
        'seat': seat,
        'seat_map': seat_map,  # Posíláme celý plán sedadel
        'form': form
    })