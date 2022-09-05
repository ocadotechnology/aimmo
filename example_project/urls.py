from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from game import urls as game_urls
from portal import urls as portal_urls

from aimmo import urls as aimmo_urls

admin.autodiscover()

urlpatterns = [
    url(r"^", include(portal_urls)),
    path("administration/", admin.site.urls),
    url(r"^rapidrouter/", include(game_urls)),
    url(r"^kurono/", include(aimmo_urls)),
]
