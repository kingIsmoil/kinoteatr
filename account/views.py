from django.shortcuts import render,redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate,logout
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect('movie_list')
    else:
        form = RegisterForm()
    return render(request, 'cinema/register.html', {'form': form})

def logoutview(request):
    logout(request)
    return redirect('login')