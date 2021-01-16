from .utils import (
    buildMenuOptions,
    getPrompt,
    removeTrailSlash,
    createNewSessionId,
    cloneStrategyRepository,
)


def test_buildMenuOptions():
    assert buildMenuOptions(["A", "B"]) == ["[a] A", "[b] B"]


def test_getPrompt(mocker):
    mocker.patch("builtins.input", return_value="toto")
    assert getPrompt("dummy prompt text") == "toto"

    mocker.patch("builtins.input", return_value="9b4db9b9-2b16-4347")
    assert getPrompt("dummy prompt text") == "9b4db9b9-2b16-4347"

    mocker.patch("builtins.input", return_value="")
    assert getPrompt("dummy prompt text", "default_value") == "default_value"


def test_removeTrailSlash():
    assert removeTrailSlash("/a/b/") == "/a/b"
    assert removeTrailSlash("a/b/") == "a/b"
    assert removeTrailSlash("/a/b") == "/a/b"


def test_createNewSessionId():
    assert len(createNewSessionId()) > 0


def test_cloneStrategyRepository():
    sessionUuid = createNewSessionId()
    cloneStrategyRepository(sessionUuid)
