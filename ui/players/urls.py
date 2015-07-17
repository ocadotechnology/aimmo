from django.conf.urls import url
from players import views
from players import api_watch

urlpatterns = [
    url(r'^$', views.home, name='home'),

    url('^accounts/register/', views.register, name='register'),

    url(r'^start_game/$', views.start_game, name='start_game'),
    url(r'^program/$', views.program, name='program'),
    url(r'^watch/$', views.watch, name='watch'),
    url(r'^statistics/$', views.statistics, name='statistics'),

    url(r'^api/code/$', views.code, name='code'),
    url(r'^api/watch/world$', api_watch.get_world_parameters, name='watch_api_world'),
    url(r'^api/watch/state$', api_watch.get_world_state, name='watch_api_state'),
]
