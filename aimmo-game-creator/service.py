#!/usr/bin/env python
import logging
import os

from worker_manager import WORKER_MANAGERS


def main():
    logging.basicConfig(level=logging.DEBUG)
    WorkerManagerClass = WORKER_MANAGERS[os.environ['WORKER_MANAGER']]
    worker_manager = WorkerManagerClass(os.environ['GAME_API_URL'])
    worker_manager.run()

if __name__ == '__main__':
    main()
