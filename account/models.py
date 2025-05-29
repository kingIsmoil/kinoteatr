from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    def __str__(self):
        return self.email

class Review(models.Model):
    star_number = models.IntegerField()
    description = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    movie_id = models.IntegerField()

    def __str__(self):
        return f"Review by {self.user.email}"