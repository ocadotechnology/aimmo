from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView
from django_js_reverse.views import urls_js
from rest_framework import routers

from aimmo import views

HOMEPAGE_REGEX = r"^kurono/"


router = routers.SimpleRouter()
router.register(r"games", views.GameViewSet)


urlpatterns = [
    url(
        r"^$",
        login_required(TemplateView.as_view(template_name="players/home.html")),
        name="kurono/home",
    ),
    url(r"^accounts/login/$", auth_views.login, name="kurono/login"),
    url(
        r"^accounts/logout/$",
        auth_views.logout,
        {"next_page": "kurono/logout_success"},
        name="kurono/logout",
    ),
    url(
        r"^accounts/logout_success/$",
        TemplateView.as_view(template_name="registration/success_logout.html"),
        name="kurono/logout_success",
    ),
    url(
        r"^play/(?P<id>[0-9]+)/$", login_required(views.watch_game), name="kurono/play"
    ),
    url(
        r"^statistics/$",
        TemplateView.as_view(template_name="players/statistics.html"),
        name="kurono/statistics",
    ),
    url(r"^api/code/(?P<id>[0-9]+)/$", views.code, name="kurono/code"),
    url(
        r"^api/games/(?P<id>[0-9]+)/users/$",
        views.GameUsersView.as_view(),
        name="kurono/game_user_details",
    ),
    url(
        r"^api/games/(?P<id>[0-9]+)/token/$",
        views.GameTokenView.as_view(),
        name="kurono/game_token",
    ),
    url(
        r"^api/games/(?P<game_id>[0-9]+)/connection_parameters/$",
        views.connection_parameters,
        name="kurono/connection_parameters",
    ),
    url(
        r"^api/games/(?P<id>[0-9]+)/complete/$",
        views.mark_game_complete,
        name="kurono/complete_game",
    ),
    url(
        r"^api/games/(?P<game_id>[0-9]+)/current_avatar/$",
        views.current_avatar_in_game,
        name="kurono/current_avatar_in_game",
    ),
    url(r"^api/", include(router.urls)),
    url(
        r"^jsreverse/$", urls_js, name="kurono/js_reverse"
    ),  # TODO: Pull request to make django_js_reverse.urls
    url(r"^games/new/$", views.add_game, name="kurono/new_game"),
    # TODO: this is a quickfix for redirecting for the Unity resources
    url(
        r"^watch/(?P<id>[0-9]+)/(?P<resource>.[0-9A-Za-z/.]+)$",
        RedirectView.as_view(url="/static/unity/%(resource)s", permanent=False),
    ),
    url(
        r"^favicon/.ico$",
        RedirectView.as_view(url="/static/favicon.ico", permanent=True),
    ),
]
