from simulation.workers.worker import Worker


class MockWorker(Worker):
    async def fetch_data(self, state_view):
        pass

    def _create_worker(self):
        pass
