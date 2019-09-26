from simulation.worker_manager import WorkerManager
from .concrete_worker import ConcreteWorker


class MockWorkerManager(WorkerManager):
    def __init__(self, *args, **kwargs):
        self.final_workers = set()
        self.updated_workers = []

        super(MockWorkerManager, self).__init__(*args, **kwargs)
        self.worker_class = ConcreteWorker

    def add_new_worker(self, player_id):
        self.final_workers.add(player_id)
        super(MockWorkerManager, self).add_new_worker(player_id)

    def delete_worker(self, player_id):
        try:
            self.final_workers.remove(player_id)
        except KeyError:
            pass
        super(MockWorkerManager, self).delete_worker(player_id)

    def update_code(self, user):
        self.updated_workers.append(user["id"])
        super(MockWorkerManager, self).update_code(user)
