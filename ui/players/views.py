from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger("views")


def home(request):
    return render(request, 'players/home.html')

@login_required
def program(request):
    return render(request, 'players/program.html')

@login_required
def code(request):
    if request.method == 'POST' :
        logger.info('POST ' + str(request.POST))
        request.user.player.code = request.POST['code']
        request.user.player.save()
        return HttpResponse("")
    else :
        logger.info('GET ' + str(request.GET))
        return HttpResponse(request.user.player.code)
        


def watch(request):
    return render(request, 'players/watch.html')


def statistics(request):
    return render(request, 'players/statistics.html')