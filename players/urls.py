from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from players import views

urlpatterns = [
    url(r'^$', staff_member_required(TemplateView.as_view(template_name='players/home.html')), name='aimmo/home'),

    url(r'^program/(?P<id>[0-9]+)/$', staff_member_required(login_required(views.ProgramView.as_view())), name='aimmo/program'),
    url(r'^program_level/(?P<num>[0-9]+)/$', staff_member_required(views.program_level), name='aimmo/program_level'),
    url(r'^watch/(?P<id>[0-9]+)/$', staff_member_required(views.watch_game), name='aimmo/watch'),
    url(r'^watch_level/(?P<num>[0-9]+)/$', staff_member_required(views.watch_level), name='aimmo/watch_level'),
    url(r'^statistics/$', staff_member_required(TemplateView.as_view(template_name='players/statistics.html')), name='aimmo/statistics'),

    url(r'^api/code/(?P<id>[0-9]+)/$', staff_member_required(views.code), name='aimmo/code'),
    url(r'^api/games/$', views.list_games, name='aimmo/games'),
    url(r'^api/games/(?P<id>[0-9]+)/$', views.get_game, name='aimmo/game_details'),
    url(r'^api/games/(?P<id>[0-9]+)/complete/$', views.mark_game_complete, name='aimmo/complete_game'),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='aimmo/js_reverse'),  # TODO: Pull request to make django_js_reverse.urls
    url(r'^games/new/$', views.add_game, name='aimmo/new_game'),
]
