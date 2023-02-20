from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import UserTuneForm, TuneForm


# Create your views here.

def home_view(request):
    context = {

    }
    return render(request, 'pages/home.html', context)

@login_required
def usertune_list_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    qs = UserTune.objects.all().filter(user=user)
    context = {
        'qs' : qs
    }
    return render(request, 'pages/tune_list.html', context)

@login_required
def usertune_detail_view(request, pk, id):
    User = get_user_model()
    user = User.objects.get(id=pk)
    usertune = get_object_or_404(UserTune, id=id, user=user)
    context = {
        'usertune':usertune
    }
    return render(request, 'pages/usertune_detail.html', context)


@login_required
def tune_create_view(request):
    form1 = TuneForm(request.POST or None)
    form2 = UserTuneForm(request.POST or None)

    if all([form1.is_valid(),form2.is_valid()]):
        parent = form1.save(commit=False)
        parent.save()
        child = form2.save(commit=False)
        child.user = request.user
        child.tune = parent
        child.save()

        return redirect('tunes-detail-view', pk=request.user.id , id=child.id)

    context = {
        'form1' : form1,
        'form2' : form2
    }
    return render(request, 'pages/tune_create_update.html', context)

@login_required
def tune_update_view(request, pk, id):
    User = get_user_model()
    user = User.objects.get(id=pk)
    usertune = get_object_or_404(UserTune, id=id, user=user)
    tune = usertune.tune
    form1 = TuneForm(request.POST or None, instance=tune)
    form2 = UserTuneForm(request.POST or None, instance=usertune)
    context = {
        'form1' : form1,
        'form2' : form2
    }
    if all([form1.is_valid(), form2.is_valid()]):
        parent = form1.save(commit=False)
        parent.save()
        child = form2.save(commit=False)
        child.user = request.user
        child.tune = parent
        child.save()
        return redirect('tunes-detail-view', pk=request.user.id , id=child.id)

    return render(request, 'pages/tune_create_update.html', context)
