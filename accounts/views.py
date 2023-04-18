from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import UserCreationForm, UserUpdateForm
from django.contrib.auth import get_user_model, login, authenticate, logout
from tunes.models import UserTune, UserTuneList
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
            next = request.GET.get('next')
            if next:
                print(next)
                return redirect(f"{next}")
            return redirect('home-view')
    context = {
    }
    return render(request, 'accounts/login_logout.html', context)

def register_user_view(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        password = form.cleaned_data['password1']
        user.set_password(password)
        user.save()

        login(request,user)
        return redirect('home-view')

    context = {
        'form':form
    }
    return render(request, 'accounts/register.html', context)

def user_profile_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    qs = UserTune.objects.filter(user=user)
    qs2 = UserTuneList.objects.filter(user=user)

    
    context = {
        'user' : user,
        'qs' : qs,
        'qs2' : qs2
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def user_profile_update_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    form = UserUpdateForm(request.POST or None, instance=user)
    if form.is_valid():
        form.save()
        return redirect('profile-view', user.id)
    
    context = {
        'form': form
    }
    return render(request, 'accounts/register.html', context)