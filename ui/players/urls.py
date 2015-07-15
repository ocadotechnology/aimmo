from django.conf.urls import url
from players import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^program/$', views.program, name='program'),
    url(r'^watch/$', views.watch, name='watch'),
    url(r'^statistics/$', views.statistics, name='statistics'),
]
