# from git import Repo
# from os import walk
# from simple_term_menu import TerminalMenu
# import yaml
# import shutil

from .utils import createNewSessionId, cleanWorkspace, prepareWorkspace


def compose():
    sessionUuid = createNewSessionId()
    prepareWorkspace(sessionUuid)
    cleanWorkspace(sessionUuid)
