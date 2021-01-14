# from unittest.mock import MagicMock
from pytest_mock import mocker
from .scaffold import getPrompt

def test_buildStrategies():
    pass

def test_getPrompt(mocker):
    mocker.patch('builtins.input', return_value="toto")
    assert getPrompt('dummy prompt text') == "toto"

    mocker.patch('builtins.input', return_value="9b4db9b9-2b16-4347-ab55-38c47bbffaee")
    assert getPrompt('dummy prompt text') == "9b4db9b9-2b16-4347-ab55-38c47bbffaee"