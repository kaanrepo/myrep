from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import UserTuneForm, TuneForm, UserTuneSearchForm, HomeSearchForm
from django.contrib.staticfiles import finders
from django.http import FileResponse, HttpResponse


# Create your views here.

def home_view(request):
    form = HomeSearchForm()
    query = request.GET.get('q')
    qs = UserTune.objects.all().filter(public=True)
    if query is not None:
        qs = UserTune.objects.search(query=query).filter(public=True)
    context = {
        'qs' : qs,
        'search_form' : form,
        'hx_url': 'hx/'
    }
    print(request.GET)
    if request.htmx:
        return render(request, 'partials/home.html', context)
    return render(request, 'pages/home.html', context)



@login_required
def usertune_list_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    query = request.GET.get('q')
    piano = request.GET.get('playonpiano')
    jam = request.GET.get('playonjamsession')
    stage = request.GET.get('playonstage')
    sheet = request.GET.get('havesheet') 

    qs = UserTune.objects.all().filter(user=user)
    if query is not None:
        qs = UserTune.objects.search(query=query).filter(user=user)

    if piano == 'on':
        qs = qs.filter(playonpiano=True)
    
    if jam == 'on':
        qs = qs.filter(playonjamsession=True)
    
    if stage == 'on':
        qs = qs.filter(playonstage=True)
    
    if sheet == 'on':
        qs = qs.filter(havesheet=True)

    search_form = UserTuneSearchForm()



    hx_url = f'/hx/tunes/{pk}'

    context = {
        'qs' : qs,
        'search_form' : search_form,
        'hx_url': hx_url
    }
    if user != request.user:
        return redirect('home-view')
    
    return render(request, 'pages/tune_list.html', context)

@login_required
def usertune_list_hx_view(request, pk):
    pass
    User = get_user_model()
    user = User.objects.get(id=pk)
    query = request.GET.get('q')
    qs = UserTune.objects.all().filter(user=user)

    piano = request.GET.get('playonpiano')
    jam = request.GET.get('playonjamsession')
    stage = request.GET.get('playonstage')
    sheet = request.GET.get('havesheet') 



    if query is not None:
        qs = UserTune.objects.search(query=query).filter(user=user)

    if piano == 'on':
        qs = qs.filter(playonpiano=True)
    
    if jam == 'on':
        qs = qs.filter(playonjamsession=True)
    
    if stage == 'on':
        qs = qs.filter(playonstage=True)
    
    if sheet == 'on':
        qs = qs.filter(havesheet=True)

    search_form = UserTuneSearchForm()
    context = {
        'qs' : qs,
        'search_form' : search_form
    }
    if user != request.user:
        return redirect('home-view')
    
    print(request.GET.get('playonpiano'))
    return render(request, 'partials/usertune_list.html', context)

def usertune_detail_view(request, pk, id):
    User = get_user_model()
    user = User.objects.get(id=pk)
    usertune = get_object_or_404(UserTune, id=id, user=user)
    context = {
        'usertune':usertune
    }
    if all([request.user != usertune.user, usertune.public == False ]):
        return redirect('home-view')
    return render(request, 'pages/usertune_detail.html', context)


@login_required
def tune_create_view(request):
    form1 = TuneForm(request.POST or None)
    form2 = UserTuneForm(request.POST or None , request.FILES)

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
    user = get_object_or_404(User, id=pk)
    usertune = get_object_or_404(UserTune, id=id, user=user)
    tune = usertune.tune
    form1 = TuneForm(request.POST or None, instance=tune)
    form2 = UserTuneForm(request.POST or None, request.FILES or None, instance=usertune)
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
    else:
        print('else')

    return render(request, 'pages/tune_create_update.html', context)

def usertune_pdf_view(request, pk, id):
    User = get_user_model()
    user = User.objects.get(id=pk)
    usertune = get_object_or_404(UserTune, id=id, user=user)
    filename = usertune.filename
    path_to_file = f'staticfiles-cdn/uploads/sheets/{pk}/{filename}'
    #path_to_file = usertune.sheet.url

    with open(path_to_file, 'rb') as f:
        response = HttpResponse(f.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline;filename={filename}'
    return response



