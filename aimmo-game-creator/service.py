#!/usr/bin/env python
import logging
import os

from worker_manager import WORKER_MANAGERS


def main():
    logging.basicConfig(level=logging.DEBUG)
    WorkerManagerClass = WORKER_MANAGERS[os.environ.get('WORKER_MANAGER', None)]
    worker_manager = WorkerManagerClass(os.environ.get('GAME_API_URL', None))
    worker_manager.run()

if __name__ == '__main__':
    main()
