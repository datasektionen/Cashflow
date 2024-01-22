from django.contrib import auth
from django.http import HttpResponseRedirect, Http404

from cashflow import settings


def login(request):
    """
    Login route, redirects to the login system.
    """
    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            settings.LOGIN_FRONTEND_URL + '/login?callback=' +
            request.scheme + '://' + request.get_host() + '/login/')
    else:
        return HttpResponseRedirect("/")


def login_with_token(request, token):
    """
    Handles a login redirect and authenticates user.
    """
    if request.method != 'GET':
        raise Http404()
    user = auth.authenticate(token=token)
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect(redirect_to=request.build_absolute_uri("/"))
    return HttpResponseRedirect("/")  # fail silently


def logout(request):
    """
    Logs out user.
    """
    auth.logout(request)
    return HttpResponseRedirect("/")
