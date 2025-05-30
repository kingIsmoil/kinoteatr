from django.db import models
from account.models import CustomUser as User


class SeatStatus(models.TextChoices):
    FREE = 'free', 'Free'
    BOOKED = 'booked', 'Booked'

class PaymentStatus(models.TextChoices):
    PAID = 'paid', 'Paid'
    UNPAID = 'unpaid', 'Unpaid'

class PaymentMethod(models.TextChoices):
    CARD = 'card', 'Карта'
    CASH = 'cash', 'Наличные'
    OTHER = 'other', 'Другое'

class UserCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    card_holder = models.CharField(max_length=100)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return f"**** **** **** {self.card_number[-4:]}"

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='movies/images/')
    duration = models.IntegerField(help_text='Duration in minutes')
    country = models.CharField(max_length=100)
    release_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title

class Actor(models.Model):
    name = models.CharField(max_length=255)
    experience = models.IntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Director(models.Model):
    fullname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

class MovieActor(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor_id = models.ForeignKey(Actor, on_delete=models.CASCADE)
    is_hero = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor_id.name} in {self.movie_id.title}"

class MovieDirector(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director_id = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.director_id.fullname} - {self.movie_id.title}"

class Trailer(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='trailers')
    file = models.FileField(upload_to='trailers/videos/')
    image = models.ImageField(upload_to='trailers/thumbnails/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Trailer for {self.movie_id.title}"

class Review(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    star_number = models.IntegerField()
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.star_number}⭐ review for {self.movie_id.title}"

class Hall(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SeatPlace(models.Model):
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='seats')
    status = models.CharField(max_length=10, choices=SeatStatus.choices, default=SeatStatus.FREE)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.hall_id.name} - {self.status}"

class Show(models.Model):
    movie_id = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='shows')
    hall_id = models.ForeignKey(Hall, on_delete=models.CASCADE, related_name='shows')
    showing_datetime = models.DateTimeField()

    def __str__(self):
        return f"{self.movie_id.title} at {self.showing_datetime.strftime('%Y-%m-%d %H:%M')} in {self.hall_id.name}"

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    show_id = models.ForeignKey(Show, on_delete=models.CASCADE, related_name='orders')
    seatplace_id = models.ForeignKey(SeatPlace, on_delete=models.CASCADE, related_name='orders')
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=10, choices=PaymentMethod.choices)
    payment_card = models.ForeignKey(UserCard, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Order by user {self.user_id} - {self.show_id.movie_id.title}"

