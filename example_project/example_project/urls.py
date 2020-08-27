from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

from aimmo import urls as aimmo_urls

admin.autodiscover()

urlpatterns = [
    url(r"^administration/", include(admin.site.urls)),
    url(r"^kurono/", include(aimmo_urls)),
    url(r"^$", RedirectView.as_view(url="/kurono")),
]
