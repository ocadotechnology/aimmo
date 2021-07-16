from unittest.mock import MagicMock

import pytest


@pytest.fixture(autouse=True)
def mock_game_manager(monkeypatch):
    """Mock GameManager for tests that don't need it."""
    monkeypatch.setattr(
        "aimmo.migrations.0025_generate_auth_token.GameManager", MagicMock()
    )
