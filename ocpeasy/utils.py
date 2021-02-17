from .constants import ALPHABET_LIST_CHAR, EMPTY_STRING, BASE_STRATEGIES_REPOSITORY

from uuid import uuid4
from git import Repo
import shutil


def prepareWorkspace(sessionUuid: str):
    PATH_SESSION = f"/tmp/{sessionUuid}"
    Repo.clone_from(f"{BASE_STRATEGIES_REPOSITORY}", PATH_SESSION)


def createNewSessionId():
    return uuid4().hex


def buildMenuOptions(arr):
    counter = 0
    options = []
    for el in arr:
        options.append(f"[{ALPHABET_LIST_CHAR[counter]}] {el}")
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


def cloneStrategyRepository(sessionId):
    PATH_SESSION = f"/tmp/{sessionId}"
    Repo.clone_from(f"{BASE_STRATEGIES_REPOSITORY}", PATH_SESSION)


def cleanWorkspace(sessionId: str):
    shutil.rmtree(f"/tmp/{sessionId}", ignore_errors=True)


def replaceAll(text: str, dic: dict):
    for i in dic.keys():
        text = text.replace(f"{i}", dic.get(i))
    return text.replace("[", "").replace("]", "")
