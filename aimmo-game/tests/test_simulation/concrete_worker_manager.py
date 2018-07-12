from simulation.worker_managers.worker_manager import WorkerManager


class ConcreteWorkerManager(WorkerManager):
    def __init__(self, *args, **kwargs):
        self.final_workers = set()
        self.clear()
        super(ConcreteWorkerManager, self).__init__(*args, **kwargs)

    def clear(self):
        self.removed_workers = []
        self.added_workers = []

    def create_worker(self, player_id):
        self.added_workers.append(player_id)
        self.final_workers.add(player_id)

    def remove_worker(self, player_id):
        self.removed_workers.append(player_id)
        try:
            self.final_workers.remove(player_id)
        except KeyError:
            pass
