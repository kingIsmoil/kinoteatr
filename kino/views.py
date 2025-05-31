from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.utils.timezone import now
from django.contrib.auth.decorators import login_required
from .forms import ReviewForm, PaymentForm
from django.contrib import messages
from datetime import datetime, timedelta

def movie_list(request):
    movies = Movie.objects.filter(is_active=True)
    today = now().date()
    tomorrow = today + timedelta(days=1)

    # Получаем параметр даты из GET-запроса
    date_filter = request.GET.get('date')
    selected_date = today  # по умолчанию

    # Получаем все доступные даты с сеансами
    available_dates = Show.objects.filter(
        showing_datetime__gte=now(),
        movie_id__in=movies
    ).dates('showing_datetime', 'day').distinct()

    shows = Show.objects.filter(
        showing_datetime__gte=now(),
        movie_id__in=movies
    )

    if date_filter:
        try:
            selected_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            shows = shows.filter(showing_datetime__date=selected_date)
        except ValueError:
            # Если неправильная дата, показываем на сегодня
            selected_date = today
            shows = shows.filter(showing_datetime__date=today)
    else:
        # По умолчанию — сегодня
        shows = shows.filter(showing_datetime__date=today)

    # Группируем фильмы с их сеансами
    movies_with_shows = []
    for movie in movies:
        movie_shows = shows.filter(movie_id=movie)
        if movie_shows.exists():
            movies_with_shows.append({
                'movie': movie,
                'shows': movie_shows
            })

    context = {
        'movies_with_shows': movies_with_shows,
        'available_dates': available_dates,
        'selected_date': selected_date.strftime('%Y-%m-%d'),
        'today': today.strftime('%Y-%m-%d'),
        'tomorrow': tomorrow.strftime('%Y-%m-%d'),
    }
    return render(request, 'cinema/movie_list.html', context)


# ... остальные функции представления остаются без изменений ...

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
    seat = get_object_or_404(SeatPlace, id=seat_id)
    show = get_object_or_404(Show, id=show_id)
    
    if seat.status != 'free':
        messages.error(request, 'Это место уже занято')
        return redirect('show_seats', show_id=show_id)
    
    if request.method == 'POST':
        form = PaymentForm(request.user, request.POST)
        if form.is_valid():
            seat.status = 'booked'
            seat.save()
            
            payment_method = form.cleaned_data['payment_method']
            payment_card = form.cleaned_data.get('card')
            
            order = Order.objects.create(
                user_id=request.user,
                show_id=show,
                seatplace_id=seat,
                payment_status='paid',
                payment_method=payment_method,
                payment_card=payment_card if payment_method == 'card' else None
            )
            
            messages.success(request, 'Бронирование успешно завершено!')
            return redirect('movie_list')
    else:
        form = PaymentForm(request.user)
    
    context = {
        'form': form,
        'seat': seat,
        'show': show,
    }
    return render(request, 'cinema/payment.html', context)

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


@login_required
def add_card(request):
    if request.method == 'POST':
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        card_holder = request.POST.get('card_holder')
        
        if len(card_number) != 16 or not card_number.isdigit():
            messages.error(request, 'Некорректный номер карты')
        else:
            UserCard.objects.create(
                user=request.user,
                card_number=card_number,
                expiry_date=expiry_date,
                card_holder=card_holder
            )
            messages.success(request, 'Карта успешно добавлена')
            return redirect('payment_info')
    
    return render(request, 'cinema/add_card.html')

@login_required
def payment_info(request):
    cards = UserCard.objects.filter(user=request.user)
    return render(request, 'cinema/payment_info.html', {'cards': cards})