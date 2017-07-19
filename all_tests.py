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

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
APPS = ('', 'aimmo-game/', 'aimmo-game-worker/', 'aimmo-game-creator/', 'integration-tests/')

def print_help():
    print(globals()['__docstring__'])


def main():
    if '--help' in sys.argv or '-h' in sys.argv:
        print_help()
        sys.exit(0)
    else:
        compute_coverage = '--coverage' in sys.argv or '-c' in sys.argv
        sys.exit(run_tests(compute_coverage))


def run_tests(compute_coverage):
    def app_name(app):
        return 'players' if app == '' else app

    failed_apps = []
    for app in APPS:
        print('Testing {}'.format(app))

        dir = os.path.join(BASE_DIR, app)
        if compute_coverage and app != '':
            result = subprocess.call(['coverage', 'run', '--concurrency=eventlet', '--source=.', 'setup.py', 'test'], cwd=dir)
        else:
            result = subprocess.call([sys.executable, 'setup.py', 'test'], cwd=dir)
        if result != 0:
            print('Tests failed: '.format(result))
            failed_apps.append(app_name(app))
    if compute_coverage:
        coverage_files = [app + '.coverage' for app in APPS]
        subprocess.call(['coverage', 'combine'] + coverage_files, cwd=BASE_DIR)
    if failed_apps:
        print('The app(s) %s had failed tests' % ', '.join(failed_apps))
        return 1
    else:
        print('All tests ran successfully')
        return 0


if __name__ == '__main__':
    main()
