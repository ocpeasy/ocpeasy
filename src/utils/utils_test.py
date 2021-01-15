from . import buildMenuOptions, getPrompt


def test_buildMenuOptions():
    assert buildMenuOptions(["A", "B"]) == ["[a] A", "[b] B"]


def test_getPrompt(mocker):
    mocker.patch("builtins.input", return_value="toto")
    assert getPrompt("dummy prompt text") == "toto"

    mocker.patch("builtins.input", return_value="9b4db9b9-2b16-4347")
    assert getPrompt("dummy prompt text") == "9b4db9b9-2b16-4347"
