# from git import Repo
# from os import walk
from simple_term_menu import TerminalMenu
import yaml

# import shutil

from .utils import (
    buildMenuOptions,
    createNewSessionId,
    cleanWorkspace,
    prepareWorkspace,
)

from .constants import (
    MENU_CURSOR_STYLE,
    SHOW_SEARCH_HINT,
)


def getModuleTypes(PATH_MODULES: str):
    with open(PATH_MODULES) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        sortedModules = sorted(list(map(lambda x: x["kind"], data)))
        modulesList = buildMenuOptions(sortedModules)
        terminal_menu = TerminalMenu(
            modulesList,
            title="Select a module type:",
            menu_cursor_style=MENU_CURSOR_STYLE,
            show_search_hint=SHOW_SEARCH_HINT,
        )
        menu_entry_index = terminal_menu.show()
        return sortedModules[menu_entry_index]


def getModulesPerKind(PATH_MODULES: str, moduleId: str):
    pass


def compose():
    sessionUuid = createNewSessionId()
    prepareWorkspace(sessionUuid)

    PATH_MODULES = f"/tmp/{sessionUuid}/modules/latest.yml"

    moduleType = getModuleTypes(PATH_MODULES)
    print(moduleType)
    cleanWorkspace(sessionUuid)
