from simulation.workers.worker import Worker


class ConcreteWorker(Worker):
    def __init__(self, *args, **kwargs):
        super(ConcreteWorker, self).__init__(*args, **kwargs)

    def _create_worker(self):
        return "http://test"

    def remove_worker(self):
        pass
