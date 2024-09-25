from functools import wraps

from django.http import HttpResponseRedirect, Http404
from django.urls import reverse

from .roles import is_member, is_admin


def login_and_team_required(login_url=None):
    return _get_decorated_function(is_member, login_url=login_url)


def team_admin_required(login_url=None):
    return _get_decorated_function(is_admin, login_url=login_url)


def _get_decorated_function(permission_test_function, login_url=None):
    def decorator(view_func):
        @wraps(view_func)
        def _inner(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                redirect_url = login_url or "account_login"
                return HttpResponseRedirect("{}?next={}".format(reverse(redirect_url), request.path))

            team = request.team  # set by middleware
            if not team or not permission_test_function(user, team):
                # treat not having access to a team like a 404 to avoid accidentally leaking information
                raise Http404

            return view_func(request, *args, **kwargs)

        return _inner

    return decorator
