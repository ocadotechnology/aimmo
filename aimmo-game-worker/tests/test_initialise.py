from httmock import all_requests, with_httmock
import initialise
import json
from os.path import join
from tempfile import mkdtemp
from unittest import TestCase

CODE = "class Avatar: pass"
OPTIONS = {'test': True}


@all_requests
def return_data(url, request):
    global url_requested
    url_requested = url
    return json.dumps({
        'code': CODE,
        'options': OPTIONS,
    })


class TestInitialise(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.TMP_DIR = mkdtemp()

    @with_httmock(return_data)
    def test_fetching_and_writing(self):
        args = ('', self.TMP_DIR)
        initialise.main(args, 'http://test', 'auth_hi')
        self.assertEqual(url_requested.geturl(), 'http://test/?auth_token=auth_hi')
        options_path = join(self.TMP_DIR, 'options.json')
        avatar_path = join(self.TMP_DIR, 'avatar.py')
        with open(options_path) as options_file:
            self.assertEqual(json.load(options_file), OPTIONS)
        with open(avatar_path) as avatar_file:
            self.assertEqual(avatar_file.read(), CODE)
