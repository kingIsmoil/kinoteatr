from django.urls import path
from . import views

urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('show/<int:show_id>/', views.show_seats, name='show_seats'),
    path('order/<int:show_id>/<int:seat_id>/', views.make_order, name='make_order'),
]
