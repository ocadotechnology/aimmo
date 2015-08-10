from django.conf.urls import url

from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required

from players import views
from players import api_watch

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='players/home.html'), name='home'),

    url('^accounts/register/', views.register, name='register'),

    url(r'^start_game/$', views.start_game, name='start_game'),
    url(r'^program/$', login_required(TemplateView.as_view(template_name='players/program.html')), name='program'),
    url(r'^watch/$', TemplateView.as_view(template_name='players/watch.html'), name='watch'),
    url(r'^statistics/$', TemplateView.as_view(template_name='players/statistics.html'), name='statistics'),

    url(r'^api/code/$', views.code, name='code'),
    url(r'^api/watch/world$', api_watch.get_world_parameters, name='watch_api_world'),
    url(r'^api/watch/state$', api_watch.get_world_state, name='watch_api_state'),
]
