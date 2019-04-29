from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import RedirectView
from django_js_reverse.views import urls_js

from aimmo import views
from app_settings import preview_user_required

HOMEPAGE_REGEX = r"^aimmo/"

urlpatterns = [
    url(
        r"^$",
        login_required(
            preview_user_required(
                TemplateView.as_view(template_name="players/home.html")
            )
        ),
        name="aimmo/home",
    ),
    url(r"^accounts/login/$", auth_views.login, name="aimmo/login"),
    url(
        r"^accounts/logout/$",
        auth_views.logout,
        {"next_page": "aimmo/logout_success"},
        name="aimmo/logout",
    ),
    url(
        r"^accounts/logout_success/$",
        TemplateView.as_view(template_name="registration/success_logout.html"),
        name="aimmo/logout_success",
    ),
    url(
        r"^play/(?P<id>[0-9]+)/$",
        login_required(preview_user_required(views.watch_game)),
        name="aimmo/play",
    ),
    url(
        r"^statistics/$",
        TemplateView.as_view(template_name="players/statistics.html"),
        name="aimmo/statistics",
    ),
    url(r"^api/csrf_token", views.csrfToken, name="aimmo/csrf_token"),
    url(r"^api/code/(?P<id>[0-9]+)/$", views.code, name="aimmo/code"),
    url(r"^api/games/$", views.list_games, name="aimmo/games"),
    url(r"^api/games/(?P<id>[0-9]+)/$", views.get_game, name="aimmo/game_details"),
    url(
        r"^api/games/(?P<game_id>[0-9]+)/connection_parameters/$",
        views.connection_parameters,
        name="aimmo/connection_parameters",
    ),
    url(
        r"^api/games/(?P<id>[0-9]+)/complete/$",
        views.mark_game_complete,
        name="aimmo/complete_game",
    ),
    url(
        r"^api/games/(?P<game_id>[0-9]+)/current_avatar/$",
        views.current_avatar_in_game,
        name="aimmo/current_avatar_in_game",
    ),
    url(
        r"^jsreverse/$", urls_js, name="aimmo/js_reverse"
    ),  # TODO: Pull request to make django_js_reverse.urls
    url(r"^games/new/$", views.add_game, name="aimmo/new_game"),
    # TODO: this is a quickfix for redirecting for the Unity resources
    url(
        r"^watch/(?P<id>[0-9]+)/(?P<resource>.[0-9A-Za-z/.]+)$",
        RedirectView.as_view(url="/static/unity/%(resource)s", permanent=False),
    ),
]
