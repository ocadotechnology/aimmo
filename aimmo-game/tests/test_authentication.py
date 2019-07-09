import secrets
from base64 import b64encode as encode

import kubernetes
import pytest

from authentication import _decode_token_from_secret

TOKEN_MAX_LENGTH = 24


@pytest.fixture
def secret():
    """
    Gives a kubernetes secret object similar to the one received by the game when
    retrieving its secret. The token is randomly generated as it would be in practice,
    uses less bytes to prevent random test failure.
    """
    test_token = encode(secrets.token_urlsafe(nbytes=12).encode("utf-8"))
    return kubernetes.client.V1Secret(
        kind="Secret",
        data={"token": test_token},
        metadata=kubernetes.client.V1ObjectMeta(
            name="Test-Secret", namespace="default"
        ),
    )


def test_get_token_from_secret(secret):
    """
    Tests that we can correctly retrieve a token from the Kubernetes secret object.

    Note this is not an actual secret that would be on a cluster, it is the object returned
    when listing/reading these secrets.
    """
    token = None
    token = _decode_token_from_secret(secret)
    assert token
    assert isinstance(token, str)
    assert len(token) <= TOKEN_MAX_LENGTH
