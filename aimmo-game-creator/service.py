#!/usr/bin/env python
from worker_manager import WORKER_MANAGERS
import logging
import os


def main():
    logging.basicConfig(level=logging.DEBUG)
    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', 'local')]
    url = os.environ.get('GAMES_API_URL', 'http://localhost:8000/players/api/games/')
    auth_token = os.environ.get('AUTH_TOKEN', 'insecure-creator-auth-token')
    worker_manager = WorkerManagerClass(url+'?auth_token='+auth_token)
    worker_manager.run()

if __name__ == '__main__':
    main()
