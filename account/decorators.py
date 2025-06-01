from django.shortcuts import redirect
from functools import wraps

def user_not_authenticated(function=None):
    @wraps(function)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('movie_list')
        return function(request, *args, **kwargs)
    return wrapper 