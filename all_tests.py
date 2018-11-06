#!/usr/bin/env python
"""Run all tests for the project.

Usage:
    run_tests.py [--coverage]

Optional arguments:
    -c, --coverage  compute the coverage while running tests.
"""

import os
import subprocess
import sys
import docker
from aimmo_runner import runner, docker_scripts


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ALL_APPS = ('aimmo/', 'integration_tests/', 'aimmo-game-creator/', 'aimmo-game/', 'aimmo-game-worker/')
APPS = ('aimmo/', 'integration_tests/')

def print_help():
    print(globals()['__docstring__'])


def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    else:
        compute_coverage = '--coverage' in sys.argv or '-c' in sys.argv
        use_docker ='--docker=false' not in sys.argv 
        runner.run_command(['pip', 'install', '-e', BASE_DIR])
        sys.exit(run_tests(compute_coverage, use_docker=use_docker))


def run_tests(compute_coverage, use_docker=True):
    failed_apps = []
    if use_docker:
        client = docker.from_env()
        docker_scripts.build_docker_images(build_target='tester')
        run_game_creator_tests(client)
        run_game_tests(client)
        run_worker_tests(client)
    else:
        # If we don't want to use docker we just run all the tests as before
        APPS = ALL_APPS 

    for app in APPS:
        print('Testing {}'.format(app))
        dir = os.path.join(BASE_DIR, app)
        if compute_coverage and app != '':
            result = subprocess.call(['coverage', 'run', '--concurrency=eventlet',
                                      '--source=.', 'setup.py', 'test'], cwd=dir)
        else:
            result = subprocess.call([sys.executable, 'setup.py', 'test'], cwd=dir)
        if result != 0:
            print('Tests failed: '.format(result))
            failed_apps.append(app)

    if compute_coverage:
        coverage_files = [app + '.coverage' for app in APPS]
        subprocess.call(['coverage', 'combine'] + coverage_files, cwd=BASE_DIR)

    if failed_apps:
        print('The app(s) %s had failed tests' % ', '.join(failed_apps))
        return 1
    else:
        print('All tests ran successfully')
        return 0

def run_game_creator_tests(client):
    client.containers.run(
        name='aimmo-game-creator-tester',
        image='ocadotechnology/aimmo-game-creator:test'
    )

def run_game_tests(client):
    client.containers.run(
        name="aimmo-game-tester",
        image='ocadotechnology/aimmo-game:test'
    )

def run_worker_tests(client):
    client.containers.run(
        name="aimmo-worker-tester",
        image='ocadotechnology/aimmo-game-worker:test',
    )

if __name__ == '__main__':
    main()
