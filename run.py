import subprocess
import sys
import time

if __name__ == '__main__':
    import os

    sys.path.append('example_project')
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example_project.settings")


from django.contrib.auth.models import User
from subprocess import CalledProcessError


def log(message):
    print >> sys.stderr, message


def run_command(args):
    try:
        subprocess.check_call(args)
    except CalledProcessError as e:
        log('Command failed with exit status %d: %s' % (e.returncode, ' '.join(args)))
        raise


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


def create_superuser_if_missing(username, password):
    try:
        User.objects.get_by_natural_key(username)
    except User.DoesNotExist:
        log('Creating superuser %s with password %s' % (username, password))
        User.objects.create_superuser(username=username, email='admin@admin.com', password=password)


def main():
    create_superuser_if_missing(username='admin', password='admin')

    server_args = []

    run_command(['pip', 'install', '-e', '.'])
    run_command(['python', './example_project/manage.py', 'migrate', '--noinput'])
    run_command(['python', './example_project/manage.py', 'collectstatic', '--noinput'])

    server = run_command_async(['python', './example_project/manage.py', 'runserver'] + server_args)
    time.sleep(2)
    game = run_command_async(['python', './aimmo-game/service.py', '127.0.0.1', '5000'])

    server.wait()
    game.wait()


if __name__ == '__main__':
    try:
        main()
    finally:
        cleanup_processes()
