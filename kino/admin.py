from django.contrib import admin
from .models import (
    Genre, Movie, Actor, Director, MovieActor, MovieDirector,
    Trailer, Review, Hall, SeatPlace, Show, Order,UserCard
)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'country', 'release_date', 'is_active')

@admin.register(UserCard)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('card_number',)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'experience', 'is_active')

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'fullname', 'is_active')

@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'actor_id', 'is_hero')

@admin.register(MovieDirector)
class MovieDirectorAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'director_id')

@admin.register(Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'is_active', 'created_at')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'user_id', 'star_number', 'is_active')

@admin.register(Hall)
class HallAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(SeatPlace)
class SeatPlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'hall_id', 'status', 'price')

@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie_id', 'hall_id', 'showing_datetime')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'show_id', 'seatplace_id', 'payment_status', 'created_at')
