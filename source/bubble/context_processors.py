def profile_context(request):
    if request.user.is_anonymous:
        return {'profile': None}
    return {'profile': request.user.profile}
