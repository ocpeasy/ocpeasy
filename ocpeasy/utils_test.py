from .utils import (
    buildMenuOptions,
    getPrompt,
    removeTrailSlash,
    createNewSessionId,
    cloneStrategyRepository,
    cleanWorkspace,
    replaceAll,
    prepareWorkspace,
)

from os import path


def test_prepareWorkspace():
    sessionUuid = createNewSessionId()
    prepareWorkspace(sessionUuid, None)
    pathToCheck = f"/tmp/{sessionUuid}/openshift_3_4/profiles/defaultApp/route.yaml"
    assert path.exists(pathToCheck)
    cleanWorkspace(sessionUuid)


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
    cloneStrategyRepository(sessionUuid, None)
    sessionWorkspace = f"/tmp/{sessionUuid}"
    assert path.exists(sessionWorkspace)
    cleanWorkspace(sessionUuid)
    assert not path.exists(sessionWorkspace)


def test_replaceAll():
    assert replaceAll("[[containerId]]", {"containerId": "helloWorld"}) == "helloWorld"
