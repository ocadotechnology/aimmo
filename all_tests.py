#!/usr/bin/env python
import os
import subprocess
import sys


def main():
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    APPS = ('', 'aimmo-game', 'aimmo-game-worker', 'aimmo-game-creator')
    failed_apps = []
    for app in APPS:
        dir = os.path.join(BASE_DIR, app)
        result = subprocess.call([sys.executable, 'setup.py', 'test'], cwd=dir)
        if result != 0:
            if app == '':
                failed_apps.append('players')
            else:
                failed_apps.append(app)
    if failed_apps:
        print('The app(s) %s had failed tests' % ', '.join(failed_apps))
        sys.exit(1)
    else:
        print('All tests ran successfully')
        sys.exit(0)

if __name__ == '__main__':
    main()
