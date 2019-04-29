import mock
from unittest import TestCase
from requests import Response
from simulation.workers.worker import Worker
from tests.test_simulation.concrete_worker import ConcreteWorker


DEFAULT_RESPONSE_CONTENT = (
    b'{"action": "test_action",' b'"log": "test_log",' b'"avatar_updated": "True"}'
)

MISSING_KEY_RESPONSE_CONTENT = (
    b'{"corruptedKey": "test_action",'
    b'"log": "test_log",'
    b'"avatar_updated": "True"}'
)


def construct_test_response(status_code=200, response_content=DEFAULT_RESPONSE_CONTENT):
    post_response = Response()
    post_response.status_code = status_code
    post_response._content = response_content
    return post_response


class TestWorker(TestCase):
    def setUp(self):
        self.worker = ConcreteWorker(1, 0)

    @mock.patch(
        "simulation.workers.worker.requests.post",
        return_value=construct_test_response(),
    )
    def test_fetch_data_fetches_correct_response(self, mocked_post):
        self.worker.fetch_data(state_view={})

        mocked_post.assert_called_once()
        self.assertEqual(self.worker.serialized_action, "test_action")
        self.assertEqual(self.worker.log, "test_log")
        self.assertEqual(self.worker.has_code_updated, "True")

    def test_setting_defaults_works_correctly(self):
        self.worker.log = "test_log_fake"
        self.worker.serialised_action = "test_action_fake"
        self.worker.has_code_updated = "test_avatar_updated_fake"

        self.worker._set_defaults()

        self.assertIsNone(self.worker.serialized_action)
        self.assertIsNone(self.worker.log)
        self.assertFalse(self.worker.has_code_updated)

    @mock.patch(
        "simulation.workers.worker.requests.post",
        return_value=construct_test_response(status_code=500),
    )
    @mock.patch.object(target=Worker, attribute="_set_defaults")
    def test_fetch_data_cannot_connect_to_worker(
        self, mocked_set_defaults, mocked_post
    ):
        self.worker.fetch_data(state_view={})

        mocked_post.assert_called_once()
        mocked_set_defaults.assert_called_once()

    @mock.patch(
        "simulation.workers.worker.requests.post",
        return_value=construct_test_response(
            response_content=MISSING_KEY_RESPONSE_CONTENT
        ),
    )
    @mock.patch.object(target=Worker, attribute="_set_defaults")
    def test_missing_key_in_worker_data(self, mocked_set_defaults, mocked_post):
        self.worker.fetch_data(state_view={})

        mocked_post.assert_called_once()
        mocked_set_defaults.assert_called_once()
