from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Review

def home(request):
    if request.user.is_authenticated:
        return redirect('user_reviews')
    return redirect('login')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone_number = request.POST.get('phone_number')
        age = request.POST.get('age')

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
            age=age
        )
        login(request, user)
        return redirect('user_reviews')
    return render(request, 'account/register.html')

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user_reviews')
    return render(request, 'account/login.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def create_review(request):
    if request.method == 'POST':
        Review.objects.create(
            star_number=request.POST.get('star_number'),
            description=request.POST.get('description'),
            movie_id=request.POST.get('movie_id'),
            user=request.user
        )
        return redirect('user_reviews')
    return render(request, 'account/create_review.html')

@login_required
def get_user_reviews(request):
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'account/user_reviews.html', {'reviews': reviews})
