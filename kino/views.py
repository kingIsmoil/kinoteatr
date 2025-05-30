# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import *
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm
from django.contrib import messages

def movie_list(request):
    movies = Movie.objects.filter(is_active=True)
    shows = Show.objects.filter(showing_datetime__gte=now()).order_by('showing_datetime')
    context = {
        'movies': movies,
        'shows': shows,
    }
    return render(request, 'cinema/movie_list.html', context)

def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    trailers = Trailer.objects.filter(movie_id=movie_id, is_active=True)
    reviews = Review.objects.filter(movie_id=movie_id, is_active=True)
    shows = Show.objects.filter(movie_id=movie_id, showing_datetime__gte=now()).order_by('showing_datetime')
    
    context = {
        'movie': movie,
        'trailers': trailers,
        'reviews': reviews,
        'shows': shows,
    }
    return render(request, 'cinema/movie_detail.html', context)




def show_seats(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    seats = SeatPlace.objects.filter(hall_id=show.hall_id).order_by('id')
    context = {
        'show': show,
        'seats': seats,
    }
    return render(request, 'cinema/show_seats.html', context)

@login_required(login_url='login')
def make_order(request, show_id, seat_id):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')  # Перенаправляем неавторизованных пользователей на страницу входа
            
        seat = get_object_or_404(SeatPlace, id=seat_id)
        if seat.status == 'free':
            seat.status = 'booked'
            seat.save()
            Order.objects.create(
                user_id=request.user,  # Передаем объект пользователя, а не ID
                show_id_id=show_id,
                seatplace_id_id=seat_id,
                payment_status='paid'  
            )
            return redirect('movie_list')
    return redirect('show_seats', show_id=show_id)

@login_required
def my_orders(request):
    orders = Order.objects.filter(user_id=request.user).select_related('show_id', 'seatplace_id', 'show_id__movie_id')
    return render(request, 'cinema/my_orders.html', {'orders': orders})

@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie_id = movie
            review.user_id = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно добавлен!')
            return redirect('movie_detail', movie_id=movie.id)
    else:
        form = ReviewForm()
    
    return render(request, 'cinema/add_review.html', {'form': form, 'movie': movie})
