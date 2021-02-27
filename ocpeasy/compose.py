# EXPERIMENTAL
from os import path, getenv
from simple_term_menu import TerminalMenu
import yaml

from .utils import (
    buildMenuOptions,
    createNewSessionId,
    cleanWorkspace,
    prepareWorkspace,
    removeTrailSlash,
)

from .constants import MENU_CURSOR_STYLE, SHOW_SEARCH_HINT, OCPEASY_CONFIG_NAME
from .notify import missingConfigurationFile, ocpeasyConfigFileUpdated


def getModuleTypes(PATH_MODULES: str):
    with open(PATH_MODULES) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        sortedModules = list(set(sorted(list(map(lambda x: x["kind"], data)))))
        modulesList = buildMenuOptions(sortedModules)
        terminal_menu = TerminalMenu(
            modulesList,
            title="Select a module type:",
            menu_cursor_style=MENU_CURSOR_STYLE,
            show_search_hint=SHOW_SEARCH_HINT,
        )
        menu_entry_index = terminal_menu.show()
        return sortedModules[menu_entry_index]


def getModulesPerKind(PATH_MODULES: str, moduleKindId: str):
    with open(PATH_MODULES) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        filteredRecords = list(
            (filter(lambda x: x["kind"] == moduleKindId, data))
        )  # noqa: E501
        modulesForKind = list(map(lambda x: x["id"], filteredRecords))
        modulesList = buildMenuOptions(modulesForKind)
        terminal_menu = TerminalMenu(
            modulesList,
            title="Select a module type:",
            menu_cursor_style=MENU_CURSOR_STYLE,
            show_search_hint=SHOW_SEARCH_HINT,
        )
        menu_entry_index = terminal_menu.show()
        return filteredRecords[menu_entry_index]


def compose(stageId: str = None, proxy: str = None):
    # TODO: select one or more stage to which module is required

    projectDevPath = getenv("PROJECT_DEV_PATH", None)
    pathProject = "." if not projectDevPath else removeTrailSlash(projectDevPath)

    ocpPeasyConfigFound = False
    ocpPeasyConfigPath = f"{pathProject}/{OCPEASY_CONFIG_NAME}"

    if path.isfile(ocpPeasyConfigPath):
        ocpPeasyConfigFound = True
    else:
        missingConfigurationFile()
        return

    if ocpPeasyConfigFound:
        sessionUuid = createNewSessionId()
        prepareWorkspace(sessionUuid)
        PATH_MODULES = f"/tmp/{sessionUuid}/modules/latest.yml"
        moduleType = getModuleTypes(PATH_MODULES)
        moduleSelected = getModulesPerKind(PATH_MODULES, moduleType)

        excludedKeys = ["module"]
        for excluded in excludedKeys:
            del moduleSelected[excluded]

        globalValues = None
        # get current configuration
        with open(ocpPeasyConfigPath) as ocpPeasyConfigFile:
            deployConfigDict = yaml.load(ocpPeasyConfigFile, Loader=yaml.FullLoader)
            globalValues = dict(deployConfigDict)

            # modulesChanged = False
            for el in globalValues["stages"]:
                modules = el.get("modules", [])
                if stageId and el.get("stageId") == stageId or stageId is None:
                    modules.append(moduleSelected)
                    el["modules"] = modules

        with open(ocpPeasyConfigPath, "w") as ocpPeasyConfigFile:
            ocpPeasyConfigFile.write(yaml.dump(globalValues))

        ocpeasyConfigFileUpdated()
        cleanWorkspace(sessionUuid)

    else:
        missingConfigurationFile()
        return
