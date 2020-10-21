import datetime

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from bubble import forms, models


def common_context(request, page='', **kwargs):
    if request.user.is_anonymous:
        profile = None
    else:
        profile = request.user.profile

    kwargs.update({
        'profile': profile,
        'active_page': page,
        'active_group': page.split('_')[0],
    })
    return kwargs

def landing(request):
    context = common_context(request, 'landing')
    return render(request, 'landing.html', context)

@login_required
def home(request):
    context = common_context(request, 'home')
    return render(request, 'home.html', context)

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
    context = common_context(request, 'login',
        form=form,
        error=error,
    )
    return render(request, 'login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('landing')

@login_required
def profile(request):
    context = common_context(request, 'profile')
    return render(request, 'profile.html', context)


@login_required
def document_list(request):
    qs = models.Document.objects.filter(profile=request.user.profile).order_by('-date', '-created')
    context = common_context(request, 'document_list', documents=qs)
    return render(request, 'document_list.html', context)

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
    context = common_context(request, 'document_create',
        form=form or forms.DocumentForm(),
        form2=forms.FileForm(),
        files=models.File.objects.filter(document=None),
    )
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
    context = common_context(request, 'document_view', document=doc)
    return render(request, 'document_view.html', context)

@login_required
def document_delete(request, pk):
    models.Document.objects.filter(pk=pk, profile=request.user.profile).delete()
    return redirect('document-list')

@login_required
def vaccine_list(request):
    context = common_context(request, 'vaccine_list')
    return render(request, 'vaccine_list.html', context)

@login_required
def vaccine_create(request):
    context = common_context(request, 'vaccine_create')
    return render(request, 'vaccine_create.html', context)

@login_required
def vaccine_view(request, pk):
    context = common_context(request, 'vaccine_view')
    return render(request, 'vaccine_view.html', context)


@login_required
def group_list(request):
    context = common_context(request, 'group_list')
    return render(request, 'group_list.html', context)

@login_required
def group_create(request):
    context = common_context(request, 'group_create')
    return render(request, 'group_create.html', context)

@login_required
def group_view(request, pk):
    context = common_context(request, 'group_view')
    return render(request, 'group_view.html', context)
