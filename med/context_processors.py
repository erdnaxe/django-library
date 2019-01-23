from .settings import SITE_NAME


def context_user(request):
    user = request.user
    is_perm = user.has_perms(['perm'])
    is_bureau = user.has_perms(['bureau'])
    return {
        'is_perm': is_perm,
        'is_bureau': is_bureau,
        'request_user': user,
        'site_name': SITE_NAME,
    }
