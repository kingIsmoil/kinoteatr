from django.shortcuts import render, get_object_or_404, redirect
from .models import Movie, Show, SeatPlace, Order
from django.utils.timezone import now

def movie_list(request):
    movies = Movie.objects.filter(is_active=True)
    shows = Show.objects.filter(showing_datetime__gte=now()).order_by('showing_datetime')
    context = {
        'movies': movies,
        'shows': shows,
    }
    return render(request, 'cinema/movie_list.html', context)

def show_seats(request, show_id):
    show = get_object_or_404(Show, id=show_id)
    seats = SeatPlace.objects.filter(hall_id=show.hall_id).order_by('id')
    context = {
        'show': show,
        'seats': seats,
    }
    return render(request, 'cinema/show_seats.html', context)

def make_order(request, show_id, seat_id):
    if request.method == 'POST':
        user_id = request.user.id if request.user.is_authenticated else 1
        seat = get_object_or_404(SeatPlace, id=seat_id)
        if seat.status == 'free':
            seat.status = 'booked'
            seat.save()
            Order.objects.create(
                user_id=user_id,
                show_id_id=show_id,
                seatplace_id_id=seat_id,
                payment_status='paid'  
            )
            return redirect('movie_list')
    return redirect('show_seats', show_id=show_id)
