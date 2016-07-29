from os import path
worker_dir = path.dirname(path.dirname(__file__))
__path__.append(worker_dir)
