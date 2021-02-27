from .constants import ALPHABET_LIST_CHAR, EMPTY_STRING, BASE_STRATEGIES_REPOSITORY

from uuid import uuid4
from git import Repo
import shutil


def prepareWorkspace(sessionUuid: str, proxy: str = None):
    cloneStrategyRepository(sessionUuid, proxy)


def createNewSessionId():
    return uuid4().hex


def buildMenuOptions(arr):
    counter = 0
    options = []
    canHaveIndex = len(arr) < 35
    for el in arr:
        index = -1
        if canHaveIndex:
            if counter < len(ALPHABET_LIST_CHAR):
                index = ALPHABET_LIST_CHAR[counter]
            else:
                index = f"{counter - len(ALPHABET_LIST_CHAR)}"

        if canHaveIndex:
            options.append(f"[{index}] {el}")
        else:
            options.append(f"{el}")
        counter += 1
    return options


def getPrompt(promptText: str, default=None, rule=None):
    value = ""
    while len(value) == 0:
        value = input(
            f"{promptText} {f'(default: {default})' if default != None else EMPTY_STRING}"  # noqa: E501
        )
        if len(value) == 0 and default:
            value = default
    return value


def removeTrailSlash(uri: str):
    if uri.endswith("/"):
        uri = uri[:-1]
    return uri


def cloneStrategyRepository(sessionId: str, proxy: str = None):
    PATH_SESSION = f"/tmp/{sessionId}"
    kwargs = {"config": f"http.proxy={proxy}"} if proxy != None else {}
    Repo.clone_from(f"{BASE_STRATEGIES_REPOSITORY}", PATH_SESSION, **kwargs)


def cleanWorkspace(sessionId: str):
    shutil.rmtree(f"/tmp/{sessionId}", ignore_errors=True)


def replaceAll(text: str, dic: dict):
    for i in dic.keys():
        text = text.replace(f"{i}", dic.get(i))
    return text.replace("[", "").replace("]", "")


def writeStageYaml(sessionId: str):
    pass
