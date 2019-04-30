import os
from unittest.mock import patch

import pytest
from authentication import generate_game_token


@patch("requests.patch")
def test_token_generation_non_empty(mock_patch):
    generate_game_token("http://test")

    assert os.environ["TOKEN"]
    assert not os.environ == ""


@patch("requests.patch")
def token_generation_is_unique(mock_patch):
    generate_game_token("http://test")

    old_token = os.environ["TOKEN"]

    generate_game_token("http://test")

    assert not old_token == os.environ["TOKEN"]
