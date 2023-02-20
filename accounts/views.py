from django.shortcuts import render, redirect
from .forms import UserCreationForm
from django.contrib.auth import get_user_model, login, authenticate, logout
# Create your views here.

def login_logout_view(request):
    User = get_user_model()
    if request.user.is_authenticated:
        logout(request)
        return redirect('home-view')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            next = request.POST.get('next')
            if next:
                return redirect(f"{next}/")
            return redirect('home-view')
    context = {
    }
    return render(request, 'accounts/login_logout.html', context)

def register_user_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()

    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)