from simulation.worker_manager import WorkerManager
from .mock_worker import MockWorker


class TestWorkerManager:
    def set_up(self):
        self.worker_manager = WorkerManager()

    async def test_fetch_worker_data_is_async(self):
        """
        Creates a mock Worker and calls fetch_all_worker_data to check it returns the
        correct type. The type expected is a list, which is returned when the
        fetch_data function is correctly awaited in the worker manager, as opposed to
        the generator Class it returns if it not awaited properly.
        """
        self.set_up()
        self.worker_manager.player_id_to_worker[0] = MockWorker(1, 0000)
        data = await self.worker_manager.fetch_all_worker_data(
            self.worker_manager.player_id_to_worker
        )
        assert type(data) == list
