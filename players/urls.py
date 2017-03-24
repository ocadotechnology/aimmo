from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from players import views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='players/home.html'), name='aimmo/home'),

    url(r'^program/$', login_required(TemplateView.as_view(template_name='players/program.html')), name='aimmo/program'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^watch/$', views.WatchView.as_view(), name='aimmo/watch'),
    url(r'^statistics/$', TemplateView.as_view(template_name='players/statistics.html'), name='aimmo/statistics'),

    url(r'^api/code/$', views.code, name='aimmo/code'),
    url(r'^api/games/$', views.games, name='aimmo/games'),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='aimmo/js_reverse'),  # TODO: Pull request to make django_js_reverse.urls
]
