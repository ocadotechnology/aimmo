from django.conf.urls import url

from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required

from players import views
from players import watch_views

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='players/home.html'), name='home'),

    url('^accounts/register/', views.register, name='register'),

    url(r'^program/$', login_required(TemplateView.as_view(template_name='players/program.html')), name='program'),
    url(r'^watch/$', TemplateView.as_view(template_name='players/watch.html'), name='watch'),
    url(r'^statistics/$', TemplateView.as_view(template_name='players/statistics.html'), name='statistics'),

    url(r'^api/code/$', views.code, name='code'),
    url(r'^api/watch/state$', watch_views.get_world_state, name='get_world_state'),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),  # TODO: Pull request to make django_js_reverse.urls
]
