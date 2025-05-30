from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('reviews/create/', views.create_review, name='create_review'),
    path('reviews/', views.get_user_reviews, name='user_reviews'),
]
