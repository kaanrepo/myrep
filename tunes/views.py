from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import *
from .forms import UserTuneForm, TuneForm, UserTuneSearchForm, HomeSearchForm, UserTuneListForm
from django.contrib.staticfiles import finders
from django.http import FileResponse, HttpResponse
from django.core.paginator import Paginator, EmptyPage
import urllib.parse

# Create your views here.

def home_view(request):
    context = {

    }
    return render(request, 'pages/home.html', context)

def public_usertune_view(request):
    form = HomeSearchForm()
    query = request.GET.get('q')
    qs = UserTune.objects.all().filter(public=True).order_by('-updated')
    hx_url = f'/tunes/hx/?'
    if query is not None:
        qs = UserTune.objects.search(query=query).filter(public=True)
        hx_url += f'q={query}&'

    paginator = Paginator(qs, 3)
    page_number = request.GET.get('page')

    hx_url += 'page='
    
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)
    context = {
        'qs' : qs,
        'search_form' : form,
        'hx_url': hx_url,
        'page_obj': page_obj,
        'paginator': paginator,
    }
    if request.htmx:
        return render(request, 'partials/public_usertune.html', context)
    return render(request, 'pages/public_usertune.html', context)



@login_required
def usertune_list_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    query = request.GET.get('q')
    piano = request.GET.get('playonpiano')
    jam = request.GET.get('playonjamsession')
    stage = request.GET.get('playonstage')
    sheet = request.GET.get('havesheet') 

    qs = UserTune.objects.all().filter(user=user).order_by('-updated')

    hx_url = f'/hx/tunes/{pk}/?'


    if query is not None:
        qs = UserTune.objects.search(query=query).filter(user=user)
        hx_url += f'q={query}&'

    if piano == 'on':
        qs = qs.filter(playonpiano=True)
        hx_url += 'playonpiano=on&'

    if jam == 'on':
        qs = qs.filter(playonjamsession=True)
        hx_url += 'playonjamsession=on&'
    
    if stage == 'on':
        qs = qs.filter(playonstage=True)
        hx_url += 'playonstage=on&'
    
    if sheet == 'on':
        qs = qs.filter(havesheet=True)
        hx_url += 'havesheet=on&'

    hx_url += 'page='

    search_form = UserTuneSearchForm()

    paginator = Paginator(qs, 7)
    page_number = request.GET.get('page')

    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)



    context = {
        'paginator': paginator,
        'page_obj' : page_obj,
        'search_form' : search_form,
        'hx_url': hx_url,
    }
    if user != request.user:
        return redirect('home-view')
    
    return render(request, 'pages/tune_list.html', context)

@login_required
def usertune_list_hx_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    query = request.GET.get('q')
    qs = UserTune.objects.all().filter(user=user).order_by('-updated')

    piano = request.GET.get('playonpiano')
    jam = request.GET.get('playonjamsession')
    stage = request.GET.get('playonstage')
    sheet = request.GET.get('havesheet') 
    

    hx_url = f'/hx/tunes/{pk}/?'


    if query is not None:
        qs = UserTune.objects.search(query=query).filter(user=user)
        hx_url += f'q={query}&'

    if piano == 'on':
        qs = qs.filter(playonpiano=True)
        hx_url += 'playonpiano=on&'

    if jam == 'on':
        qs = qs.filter(playonjamsession=True)
        hx_url += 'playonjamsession=on&'
    
    if stage == 'on':
        qs = qs.filter(playonstage=True)
        hx_url += 'playonstage=on&'
    
    if sheet == 'on':
        qs = qs.filter(havesheet=True)
        hx_url += 'havesheet=on&'

    hx_url += 'page='

    search_form = UserTuneSearchForm()

    paginator = Paginator(qs, 7)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    context = {
        'paginator': paginator,
        'page_obj' : page_obj,
        'search_form' : search_form,
        'hx_url': hx_url,
    }
    if user != request.user:
        return redirect('home-view')
    
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


@login_required
def usertune_lists_view(request, pk):
    User = get_user_model()
    user = User.objects.get(id=pk)
    lists = UserTuneList.objects.filter(user=user).order_by('-updated')
    form = HomeSearchForm()
    query = request.GET.get('q')
    hx_url = f'/tunes/hx/list/{pk}/?'
    
    if query is not None:
        lists = UserTuneList.objects.search(query=query).filter(user=user).order_by('-updated')
        hx_url += f'q={query}&'


    paginator = Paginator(lists, 2)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        page_obj = paginator.get_page(1)

    hx_url += 'page='

    
    context = {
        'lists' : lists,
        'page_obj': page_obj,
        'paginator':paginator,
        'hx_url' : hx_url,
        'search_form': form
    }

    if request.htmx:
        return render(request, 'partials/usertune_lists.html', context)
    
    return render(request, 'pages/usertune_lists.html', context)

@login_required
def usertune_lists_detail_view(request, pk, id):
    list = UserTuneList.objects.get(id=id)

    context = {
        'list' : list
    }

    return render(request, 'pages/usertune_lists_detail.html', context)

@login_required
def usertune_list_create_view(request):
    form = UserTuneListForm(request.POST or None, user=request.user)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        form.save_m2m()
        return redirect('usertune-lists-view', request.user.id)
    context = {
        'form' : form
    }
    return render(request, 'pages/usertune_lists_create_update.html', context)

@login_required
def usertune_list_update_view(request, pk, id):
    User = get_user_model()
    user = User.objects.get(id=pk)
    instance = UserTuneList.objects.get(id=id)
    form = UserTuneListForm(request.POST or None, user=user, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.save()
        form.save_m2m()
        return redirect('usertune-lists-view', request.user.id)
    context = {
        'form' : form
    }
    return render(request, 'pages/usertune_lists_create_update.html', context)


@login_required
def delete_objects_view(request, model, **kwargs):
    MODELS = {
        'tune' : Tune,
        'usertune' : UserTune,
        'list' : UserTuneList
    }
    model_class = MODELS.get(model)
    if model_class is None:
        pass
    obj = get_object_or_404(model_class, **kwargs)

    if request.user != obj.user:
        return redirect('home-view')

    if request.method == 'POST':
        obj.delete()
        return redirect('home-view')
    
    context = {
        'obj' : obj
    }

    return render(request, 'pages/delete_confirmation.html', context)

