from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
     path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='cinema/login.html'), name='login'),
    path('logout/', views.logoutview, name='logout'),

]