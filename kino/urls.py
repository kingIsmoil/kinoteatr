from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('film/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('show/<int:show_id>/', views.show_seats, name='show_seats'),
    path('order/<int:show_id>/<int:seat_id>/', views.make_order, name='make_order'),
]
