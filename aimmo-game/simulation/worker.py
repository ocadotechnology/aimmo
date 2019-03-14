import logging

import requests
LOGGER = logging.getLogger(__name__)


class Worker(object):
    def __init__(self, worker_url):
        self.url = worker_url
        self.log = None
        self.code = None
        self.serialized_action = None
        self.has_code_updated = False

    def _set_defaults(self):
        self.log = None
        self.serialized_action = None
        self.has_code_updated = False

    def fetch_data(self, state_view):
        try:
            code_and_options = {
                'code': self.code,
                'options': {},
                'state': None,
            }
            data = {**state_view, **code_and_options}
            response = requests.post(self.url, json=data)
            response.raise_for_status()
            data = response.json()
            self.serialized_action = data['action']
            self.log = data['log']
            self.has_code_updated = data['avatar_updated']
        except requests.exceptions.ConnectionError:
            LOGGER.info('Could not connect to worker, probably not ready yet')
            self._set_defaults()
        except KeyError as e:
            LOGGER.error('Missing key in data from worker: {}'.format(e))
            self._set_defaults()
        except Exception as e:
            LOGGER.exception('Unknown error while fetching turn data.')
            LOGGER.exception(e)
            self._set_defaults()
