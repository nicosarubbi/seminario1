from django.shortcuts import render, redirect


def landing(request):
    context = {'profile': request.user.profile}
    return render(request, 'landing.html', context)

def home(request):
    context = {'profile': request.user.profile}
    return render(request, 'home.html', context)

def login(request):
    context = {'profile': request.user.profile}
    return render(request, 'login.html', context)

def logout(request):
    context = {'profile': request.user.profile}
    return redirect('landing', context)

def profile(request):
    context = {'profile': request.user.profile}
    return render(request, 'profile.html', context)


def document_list(request):
    context = {'profile': request.user.profile}
    return render(request, 'document_list.html', context)

def document_create(request):
    context = {'profile': request.user.profile}
    return render(request, 'document_create.html', context)

def document_view(request, pk):
    context = {'profile': request.user.profile}
    return render(request, 'document_view.html', context)


def vaccine_list(request):
    context = {'profile': request.user.profile}
    return render(request, 'vaccine_list.html', context)

def vaccine_create(request):
    context = {'profile': request.user.profile}
    return render(request, 'vaccine_create.html', context)

def vaccine_view(request, pk):
    context = {'profile': request.user.profile}
    return render(request, 'vaccine_view.html', context)



def group_list(request):
    context = {'profile': request.user.profile}
    return render(request, 'group_list.html', context)

def group_create(request):
    context = {'profile': request.user.profile}
    return render(request, 'group_create.html', context)

def group_view(request, pk):
    context = {'profile': request.user.profile}
    return render(request, 'group_view.html', context)


def group_list(request):
    context = {'profile': request.user.profile}
    return render(request, 'group_list.html', context)

def group_create(request):
    context = {'profile': request.user.profile}
    return render(request, 'group_create.html', context)

def group_view(request, pk):
    context = {'profile': request.user.profile}
    return render(request, 'group_view.html', context)

