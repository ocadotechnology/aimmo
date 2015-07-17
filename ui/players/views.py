from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from threading import Thread
from simulation.avatar_manager import AvatarManager
from simulation.level import Level
from simulation.turn_manager import TurnManager
from simulation.world_map import WorldMap
from simulation.world_state import WorldState
import logging

logger = logging.getLogger("views")

def home(request):
    return render(request, 'players/home.html')


def run_game():
    print "Running game..."
    level = Level(15, 15, 0.1, 0.1)
    world_map = WorldMap(level)
    player_manager = AvatarManager([])
    world_state = WorldState(world_map, player_manager)
    turn_manager = TurnManager(world_state)

    turn_manager.run_game()

def start_game(request):
    thread = Thread(target=run_game)
    thread.start()
    return redirect('home')

@login_required
def program(request):
    return render(request, 'players/program.html')

@login_required
def code(request):
    if request.method == 'POST' :
        logger.info('POST ' + str(request.POST))
        request.user.player.code = request.POST['code']
        request.user.player.save()
        player_manager.player_changed_code(request.user.id, request.user.player.code)
        return HttpResponse("")
    else :
        logger.info('GET ' + str(request.GET))
        return HttpResponse(request.user.player.code)
        


def watch(request):
    return render(request, 'players/watch.html')


def statistics(request):
    return render(request, 'players/statistics.html')