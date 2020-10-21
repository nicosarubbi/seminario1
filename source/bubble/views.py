from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
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

def home(request):
    context = common_context(request, 'home')
    return render(request, 'home.html', context)

def login(request):
    context = common_context(request, 'login')
    return render(request, 'login.html', context)

def logout(request):
    context = common_context(request)
    return redirect('landing')

def profile(request):
    context = common_context(request, 'profile')
    return render(request, 'profile.html', context)


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

def document_file(request):
    form = forms.FileForm(request.POST, request.FILES)
    print(request.method, request.POST)
    if form.is_valid():
        data = form.cleaned_data
        models.File.objects.create(**cleaned_data)
        return HttpResponse('')
    return HttpResponse('error')

def document_view(request, pk):
    doc = models.Document.objects.get(pk=pk)
    context = common_context(request, 'document_view', document=doc)
    return render(request, 'document_view.html', context)

def document_delete(request, pk):
    models.Document.objects.filter(pk=pk, profile=request.user.profile).delete()
    return redirect('document-list')

def vaccine_list(request):
    context = common_context(request, 'vaccine_list')
    return render(request, 'vaccine_list.html', context)

def vaccine_create(request):
    context = common_context(request, 'vaccine_create')
    return render(request, 'vaccine_create.html', context)

def vaccine_view(request, pk):
    context = common_context(request, 'vaccine_view')
    return render(request, 'vaccine_view.html', context)



def group_list(request):
    context = common_context(request, 'group_list')
    return render(request, 'group_list.html', context)

def group_create(request):
    context = common_context(request, 'group_create')
    return render(request, 'group_create.html', context)

def group_view(request, pk):
    context = common_context(request, 'group_view')
    return render(request, 'group_view.html', context)
