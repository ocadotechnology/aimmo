from django.conf.urls import include, url
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
        r"^play/(?P<id>[0-9]+)/$", login_required(views.watch_game), name="kurono/play"
    ),
    url(
        r"^statistics/$",
        TemplateView.as_view(template_name="players/statistics.html"),
        name="kurono/statistics",
    ),
    url(r"^api/code/(?P<id>[0-9]+)/$", views.code, name="kurono/code"),
    url(r"^api/badges/(?P<id>[0-9]+)/$", views.badges, name="kurono/badges"),
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
    url(r"^api/", include(router.urls)),
    url(
        r"^jsreverse/$", urls_js, name="kurono/js_reverse"
    ),  # TODO: Pull request to make django_js_reverse.urls
    url(
        r"^favicon/.ico$",
        RedirectView.as_view(url="/static/favicon.ico", permanent=True),
    ),
]
