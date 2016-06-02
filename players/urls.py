from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

from players import views

urlpatterns = [
    url(r'^$', staff_member_required(TemplateView.as_view(template_name='players/home.html')), name='home'),

    url('^accounts/register/', staff_member_required(views.register), name='register'),

    url(r'^program/$', staff_member_required(login_required(TemplateView.as_view(template_name='players/program.html'))), name='program'),
    url(r'^watch/$', staff_member_required(TemplateView.as_view(template_name='players/watch.html')), name='watch'),
    url(r'^statistics/$', staff_member_required(TemplateView.as_view(template_name='players/statistics.html')), name='statistics'),

    url(r'^api/code/$', staff_member_required(views.code), name='code'),
    url(r'^api/games/$', views.games, name='games'),

    url(r'^jsreverse/$', 'django_js_reverse.views.urls_js', name='js_reverse'),  # TODO: Pull request to make django_js_reverse.urls
]
