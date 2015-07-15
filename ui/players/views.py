from django.shortcuts import render


def home(request):
    return render(request, 'players/home.html')


def program(request):
    return render(request, 'players/program.html')


def watch(request):
    return render(request, 'players/watch.html')


def statistics(request):
    return render(request, 'players/statistics.html')