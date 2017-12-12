from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from players import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='players/home.html'), name='aimmo/home'),

    url(r'^accounts/login/$', auth_views.login),

    url(r'^program/(?P<id>[0-9]+)/$', login_required(views.ProgramView.as_view()), name='aimmo/program'),
    url(r'^program_level/(?P<num>[0-9]+)/$', login_required(views.program_level), name='aimmo/program_level'),
    url(r'^watch/(?P<id>[0-9]+)/$', login_required(views.watch_game), name='aimmo/watch'),
    url(r'^watch_level/(?P<num>[0-9]+)/$', login_required(views.watch_level), name='aimmo/watch_level'),
    url(r'^statistics/$', TemplateView.as_view(template_name='players/statistics.html'), name='aimmo/statistics'),

    url(r'^api/code/(?P<id>[0-9]+)/$', views.code, name='aimmo/code'),
    url(r'^api/games/$', views.list_games, name='aimmo/games'),
    url(r'^api/games/(?P<id>[0-9]+)/$', views.get_game, name='aimmo/game_details'),
    url(r'^api/games/(?P<id>[0-9]+)/complete/$', views.mark_game_complete, name='aimmo/complete_game'),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='aimmo/js_reverse'),  # TODO: Pull request to make django_js_reverse.urls
    url(r'^games/new/$', views.add_game, name='aimmo/new_game'),

    # TODO: this is a quickfix for redirecting for the Unity resources
    url(r'^watch/(?P<id>[0-9]+)/(?P<resource>.[0-9A-Za-z/.]+)$',
        RedirectView.as_view(url='/static/unity/%(resource)s', permanent=False)),

    url(r'^socket.io/socket.io.js',
        RedirectView.as_view(url='https://cdnjs.cloudflare.com/ajax/libs/socket.io/1.7.4/socket.io.min.js', permanent=False)),
]
