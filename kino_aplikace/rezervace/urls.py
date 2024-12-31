from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('rezervace/', views.reservation, name='reservation'),
    path('seznam_rezervaci/', views.all_reservation, name='all_reservation'),
    path('add/', views.add_film, name='add_film'),
    path('success/', views.success, name='success'),
    path('movie/<int:movie_id>/seats/', views.movie_seats, name='movie_seats'),
    path('movie/<int:movie_id>/delete/', views.delete_movie, name='delete_movie'),
    #path('movie_seats/', views.movie_seats, name='movie_seats'),
    path('movie/<int:movie_id>/seats/<int:seat_id>/reserve/', views.reserve_seat, name='reserve_seat'),
         ]