from django.conf.urls import include, url
from django.contrib import admin
from players import urls as players_urls

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include(players_urls)),
]
