from django.shortcuts import render, redirect


def common_context(request, page=''):
    if request.user.is_anonymous:
        profile = None
    else:
        profile = request.user.profile

    return {
        'profile': profile,
        'active_page': page,
        'active_group': page.split('_')[0],
    }


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
    return redirect('landing', context)

def profile(request):
    context = common_context(request, 'profile')
    return render(request, 'profile.html', context)


def document_list(request):
    context = common_context(request, 'document_list')
    return render(request, 'document_list.html', context)

def document_create(request):
    context = common_context(request, 'document_create')
    return render(request, 'document_create.html', context)

def document_view(request, pk):
    context = common_context(request, 'document_view')
    return render(request, 'document_view.html', context)


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
