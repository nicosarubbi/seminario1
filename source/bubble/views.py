import datetime

from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from bubble import forms, models


def landing(request):
    return render(request, 'landing.html')

@login_required
def home(request):
    return render(request, 'home.html', {'nav_page': 'home'})

def login_view(request):
    error = False
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next = request.GET.get('next', 'home')
            return redirect(next)
        form = AuthenticationForm(request.POST)
        error = True
    else:
        form = AuthenticationForm()
    context = {
        'form': form,
        'error': error,
    }
    return render(request, 'login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            data = form.cleaned_data
            if 'password' in data:
                request.user.set_password(data.pop('password'))
                request.user.save()
            email = data.pop('email', None)
            if email and email != request.user.email:
                request.user.email = email
                request.user.username = email
                request.user.save()
            models.Profile.objects.filter(pk=profile.pk).update(**data)
            return redirect('home')
    else:
        form = forms.ProfileForm(dict(
            email=request.user.email,
            first_name=profile.first_name,
            last_name=profile.last_name,
            nickname=profile.nickname,
            phone=profile.phone,
            birthdate=profile.birthdate,
            password='',
        ), instance=profile)
    return render(request, 'profile.html', {'form': form, 'nav_page': 'profile'})

def register(request):
    if request.method == "POST":
        form = forms.ProfileForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            email = data.pop('email')
            password = data.pop('password', None)
            user = User.objects.create(username=email, email=email)
            user.set_password(password)
            user.save()
            profile = models.Profile.objects.create(user=user, **data)
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = forms.ProfileForm()
    return render(request, 'register.html', {'form': form})

@login_required
def document_list(request):
    form = forms.FilterForm(request.GET)
    profile = request.user.profile
    qs = models.Profile.objects.filter(Q(parent=profile) | Q(pk=profile.pk))
    form.fields['profile'].queryset=qs
    if form.is_valid():
        data = form.cleaned_data
        profile = data['profile'] or profile
        qs = models.Document.query(profile=profile, query=data['q'])
    else:
        qs = models.Document.query(profile=request.user.profile, query="")
    return render(request, 'document_list.html', {'documents': qs.order_by('-date', '-created'), 'nav_page': 'document_list', 'form': form})

def document_ok(request):
    # upload file if there is any
    form = forms.FileForm(request.POST, request.FILES)
    if form.is_valid():
        file = form.cleaned_data['file']
        models.File.objects.create(
            profile=request.user.profile,
            file=file,
            name=file.name,
        )
    # save document
    form = forms.DocumentForm(request.POST)
    p = request.user.profile
    qs = models.Profile.objects.filter(Q(parent=p) | Q(pk=p.pk))
    form.fields['profile'].queryset=qs
    if form.is_valid():
        data = form.cleaned_data
        doc = models.Document.objects.create(**data)
        models.File.objects.filter(document=None).update(document=doc)
        return redirect('document-list')
    return document_continue(request, form)

def document_add(request):
    form = forms.FileForm(request.POST, request.FILES)
    if form.is_valid():
        file = form.cleaned_data['file']
        models.File.objects.create(
            profile=request.user.profile,
            file=file,
            name=file.name,
        )

def document_remove(request, id):
    models.File.objects.filter(pk=id).delete()
    return document_continue(request)

def document_continue(request, form=None):
    f = forms.DocumentForm()
    p = request.user.profile
    qs = models.Profile.objects.filter(Q(parent=p) | Q(pk=p.pk))
    f.fields['profile'].queryset=qs
    context = {
        'form': form or f,
        'form2': forms.FileForm(),
        'files': models.File.objects.filter(document=None),
        'nav_page': 'document_create',
    }
    return render(request, 'document_create.html', context)

@login_required
def document_create(request):
    if request.method == "POST":
        submit_name = request.POST["submit"]
        if submit_name == "ok":
            return document_ok(request)
        if submit_name == "add":
            document_add(request)
        if submit_name.startswith('remove-'):
            document_remove(request, submit_name.replace('remove-', ''))
        return document_continue(request, forms.DocumentForm(request.POST))
    return document_continue(request)

@login_required
def document_view(request, pk):
    doc = models.Document.objects.get(pk=pk)
    return render(request, 'document_view.html', {'document': doc})

@login_required
def document_delete(request, pk):
    models.Document.objects.filter(pk=pk, profile=request.user.profile).delete()
    return redirect('document-list')

###############################################################################################

@login_required
def vaccine_list(request):
    form = forms.FilterForm(request.GET)
    profile = request.user.profile
    qs = models.Profile.objects.filter(Q(parent=profile) | Q(pk=profile.pk))
    form.fields['profile'].queryset=qs
    if form.is_valid():
        data = form.cleaned_data
        profile = data['profile'] or profile
        qs = models.Document.query(profile=profile, query=data['q'], vaccine=True)
    else:
        qs = models.Document.query(profile=request.user.profile, query="", vaccine=True)
    return render(request, 'vaccine_list.html', {'vaccines': qs.order_by('-date', '-created'), 'nav_page': 'vaccine_list', 'form': form})

def vaccine_ok(request):
    # upload file if there is any
    form = forms.FileForm(request.POST, request.FILES)
    if form.is_valid():
        file = form.cleaned_data['file']
        models.File.objects.create(
            profile=request.user.profile,
            file=file,
            name=file.name,
        )
    # save document
    form = forms.VaccineForm(request.POST)
    p = request.user.profile
    qs = models.Profile.objects.filter(Q(parent=p) | Q(pk=p.pk))
    form.fields['profile'].queryset=qs
    if form.is_valid():
        data = form.cleaned_data
        doc = models.Document.objects.create(type="V", **data)
        models.File.objects.filter(document=None).update(document=doc)
        return redirect('vaccine-list')
    return vaccine_continue(request, form)

def vaccine_add(request):
    form = forms.FileForm(request.POST, request.FILES)
    if form.is_valid():
        file = form.cleaned_data['file']
        models.File.objects.create(
            profile=request.user.profile,
            file=file,
            name=file.name,
        )

def vaccine_remove(request, id):
    models.File.objects.filter(pk=id).delete()
    return vaccine_continue(request)

def vaccine_continue(request, form=None):
    f = forms.VaccineForm()
    p = request.user.profile
    qs = models.Profile.objects.filter(Q(parent=p) | Q(pk=p.pk))
    f.fields['profile'].queryset=qs
    context = {
        'form': form or f,
        'form2': forms.FileForm(),
        'files': models.File.objects.filter(document=None),
        'nav_page': 'vaccine_create',
    }
    return render(request, 'vaccine_create.html', context)

@login_required
def vaccine_create(request):
    if request.method == "POST":
        submit_name = request.POST["submit"]
        if submit_name == "ok":
            return vaccine_ok(request)
        if submit_name == "add":
            vaccine_add(request)
        if submit_name.startswith('remove-'):
            vaccine_remove(request, submit_name.replace('remove-', ''))
        return vaccine_continue(request, forms.VaccineForm(request.POST))
    return vaccine_continue(request)

@login_required
def vaccine_view(request, pk):
    doc = models.Document.objects.get(pk=pk)
    return render(request, 'vaccine_view.html', {'vaccine': doc})

@login_required
def vaccine_delete(request, pk):
    models.Document.objects.filter(pk=pk, profile=request.user.profile).delete()
    return redirect('vaccine-list')

###############################################################################################

@login_required
def vaccine_calendar(request):
    return render(request, 'vaccine_calendar.html', {})

@login_required
def group_list(request):
    query = request.GET.get('q', '')
    qs = models.Profile.objects.filter(parent=request.user.profile)
    return render(request, 'group_list.html', {'group': qs.order_by('last_name', 'first_name'), 'nav_page': 'group_list'})


@login_required
def group_create(request):
    if request.method == "POST":
        form = forms.GroupForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            models.Profile.objects.create(parent=request.user.profile, user=None, **data)
            return redirect('group-list')
    else:
        form = forms.GroupForm()
    context = {
    'form': form,
    'nav_page': 'group_create',
    }
    return render(request, 'group_create.html', context)  

@login_required
def group_view(request, pk):
    profile = models.Profile.objects.get(pk=pk, parent=request.user.profile)
    if request.method == "POST":
        form = forms.GroupForm(request.POST, instance=profile)
        if form.is_valid():
            data = form.cleaned_data
            models.Profile.objects.filter(pk=pk, parent=request.user.profile).update(**data)
            return redirect('group-list')
    else:
        form = forms.GroupForm(instance=profile)
    context = {
    'form': form,
    }
    return render(request, 'group_create.html', context) 

@login_required
def group_delete(request, pk):
    models.Profile.objects.filter(pk=pk, parent=request.user.profile).delete()
    return redirect('group-list')
