from django.db import models

from django.db import models

# Create your models here.

class Movie(models.Model):
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    age_limit = models.CharField(max_length=50)
    image = models.ImageField()
    duration = models.IntegerField()
    country = models.CharField(max_length=50)
    rel_year = models.BigIntegerField()
    is_active = models.BooleanField()
    created_at = models.DateTimeField()

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'movies'
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'



class Actor(models.Model):
    name = models.CharField(max_length=250)
    experience = models.models.BigIntegerField()
    is_active = models.BooleanField(default=True)
    created_at = models.BigIntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'actors'
        verbose_name = 'Actor'
        verbose_name_plural = 'Actors'

class MovieActor(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    is_hero = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.movie} - {self.actor}"
    
    class Meta:
        db_table = 'movieactors'
        verbose_name = 'MovieActor'
        verbose_name_plural = 'MovieActors'

class Director(models.Model):
    fullname = models.CharField(max_length=150)
    is_active = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname

    class Meta:
        db_table = 'directors'
        verbose_name = 'Director'
        verbose_name_plural = 'Directors'

class MovieDirector(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey(Director, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.movie} - {self.director}"
    
    class Meta:
        db_table = 'moviedirectors'
        verbose_name = 'MovieDirector'
        verbose_name_plural = 'MovieDirectors'

class Trailer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    file = models.FileField()
    image = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField()

    def __str__(self):
        return f"{self.movie}"

    class Meta:
        db_table = 'trailers'
        verbose_name = 'Trailer'
        verbose_name_plural = 'Trailers'