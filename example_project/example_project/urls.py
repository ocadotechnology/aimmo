from aimmo import urls as aimmo_urls
from django.conf.urls import include, url
from django.contrib import admin
from game import urls as game_urls
from portal import urls as portal_urls

admin.autodiscover()

urlpatterns = [
    url(r"^", include(portal_urls)),
    url(r"^administration/", include(admin.site.urls)),
    url(r"^rapidrouter/", include(game_urls)),
    url(r"^kurono/", include(aimmo_urls)),
]
