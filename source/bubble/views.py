import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
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
    return render(request, 'profile.html')


@login_required
def document_list(request):
    query = request.GET.get('q', '')
    qs = models.Document.query(profile=request.user.profile, query=query)
    return render(request, 'document_list.html', {'documents': qs.order_by('-date', '-created'), 'nav_page': 'document_list'})

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
    if form.is_valid():
        data = form.cleaned_data
        doc = models.Document.objects.create(profile=request.user.profile, **data)
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
    context = {
        'form': form or forms.DocumentForm(),
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
    query = request.GET.get('q', '')
    qs = models.Document.query(profile=request.user.profile, query=query, vaccine=True)
    return render(request, 'vaccine_list.html', {'vaccines': qs.order_by('-date', '-created'), 'nav_page': 'vaccine_list'})

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
    if form.is_valid():
        data = form.cleaned_data
        doc = models.Document.objects.create(profile=request.user.profile, type="V", **data)
        models.File.objects.filter(document=None).update(document=doc)
        return redirect('vaccine-list')
    return document_continue(request, form)

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
    context = {
        'form': form or forms.VaccineForm(),
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
    return render(request, 'group_list.html', {})

@login_required
def group_create(request):
    return render(request, 'group_create.html', {})

@login_required
def group_view(request, pk):
    return render(request, 'group_view.html', {})
