def context_user(request):
    return {
        'is_perm': request.user.has_perms(['perm']),
        'is_bureau': request.user.has_perms(['bureau']),
    }
