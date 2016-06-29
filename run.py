import subprocess
import sys
import time

from subprocess import CalledProcessError


def log(message):
    print >> sys.stderr, message


def run_command(args):
    try:
        subprocess.check_call(args)
    except CalledProcessError as e:
        log('Command failed with exit status %d: %s' % (e.returncode, ' '.join(args)))


PROCESSES = []


def run_command_async(args):
    p = subprocess.Popen(args)
    PROCESSES.append(p)
    return p


def cleanup_processes():
    for p in PROCESSES:
        try:
            p.terminate()
            time.sleep(0.9)
            p.kill()
        except:
            pass


def main():
    server_args = []

    run_command(['pip', 'install', '-e', '.'])
    run_command(['./example_project/manage.py', 'migrate', '--noinput'])
    run_command(['./example_project/manage.py', 'collectstatic', '--noinput'])

    server = run_command_async(['./example_project/manage.py', 'runserver'] + server_args)
    time.sleep(2)
    game = run_command_async(['./aimmo-game/service.py', '127.0.0.1', '5000'])

    server.wait()
    game.wait()


if __name__ == '__main__':
    try:
        main()
    finally:
        cleanup_processes()
