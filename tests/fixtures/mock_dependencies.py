import os
import pytest
from unittest import MagicMock

@pytest.fixture(scope="session", autouse=True)
def mock_dependencies():
    if bool(os.getenv("GITHUB_ACTIONS")):
        whisper = MagicMock()
        ChatOllama = MagicMock()
        YouTubeDL = MagicMock()

        return whisper, ChatOllama, YouTubeDL

# TODO: Mock dependencies in test functions
# TODO: Inject dependencies in client.py
# TODO: Invert dependencies
