from django.shortcuts import render
from django.contrib.auth import get_user_model
from .models import *


# Create your views here.

def home_view(request):
    context = {

    }
    return render(request, 'pages/home.html', context)

def tune_list_view(request, username):
    User = get_user_model()
    user = User.objects.get(username=request.user)
    qs = UserTune.objects.all().filter(user=user)
    context = {
        'qs' : qs
    }
    return render(request, 'pages/tune_list.html', context)

def tune_detail_view(request, username, id):
    usertune = UserTune.objects.get(id=id)
    context = {
        'usertune':usertune
    }
    return render(request, 'pages/tune_detail.html', context)
