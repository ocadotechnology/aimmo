from simulation.worker_managers.worker_manager import WorkerManager


class ConcreteWorkerManager(WorkerManager):
    def __init__(self, *args, **kwargs):
        self.final_workers = set()
        self.removed_workers = []
        self.updated_workers = []
        self.added_workers = []

        super(ConcreteWorkerManager, self).__init__(*args, **kwargs)

    def create_worker(self, player_id):
        self.added_workers.append(player_id)
        self.final_workers.add(player_id)

    def remove_worker(self, player_id):
        self.removed_workers.append(player_id)
        try:
            self.final_workers.remove(player_id)
        except KeyError:
            pass

    def update_code(self, user):
        self.updated_workers.append(user['id'])
        super(ConcreteWorkerManager, self).update_code(user)
