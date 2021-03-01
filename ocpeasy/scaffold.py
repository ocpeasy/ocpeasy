from git import Repo
from os import walk
from simple_term_menu import TerminalMenu
import yaml
import shutil

from .utils import (
    buildMenuOptions,
    getPrompt,
    removeTrailSlash,
    createNewSessionId,
    cleanWorkspace,
    prepareWorkspace,
)

from .constants import (
    MENU_CURSOR_STYLE,
    PREFIX_STRATEGY,
    SHOW_SEARCH_HINT,
    OCPEASY_CONFIG_NAME,
    PLATFORM_LABEL,
)


def getStrategyVersions(sessionUuid: str):
    PATH_SESSION = f"/tmp/{sessionUuid}"
    _, folders, _ = next(walk(PATH_SESSION))
    strategies = list(filter(lambda x: x.startswith(PREFIX_STRATEGY), folders))
    strategiesOptions = [
        f'{PLATFORM_LABEL} {el.replace(PREFIX_STRATEGY, "").replace("_", ".")}'
        for el in strategies
    ]
    terminal_menu = TerminalMenu(
        buildMenuOptions(strategiesOptions),
        title="Select an OpenShift strategy:",
        menu_cursor_style=MENU_CURSOR_STYLE,
        show_search_hint=SHOW_SEARCH_HINT,
    )
    menu_entry_index = terminal_menu.show()
    return strategies[menu_entry_index]


def getTechnology(PATH_TEMPLATES: str):
    with open(PATH_TEMPLATES) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        sortedTechnologies = list(
            set(sorted(list(map(lambda x: x["technology"], data))))
        )
        technologies = buildMenuOptions(sortedTechnologies)
        terminal_menu = TerminalMenu(
            technologies,
            title="Select a technology:",
            menu_cursor_style=MENU_CURSOR_STYLE,
            show_search_hint=SHOW_SEARCH_HINT,
        )
        menu_entry_index = terminal_menu.show()
        return sortedTechnologies[menu_entry_index]


def getFramework(PATH_TEMPLATES: str, technology: str):
    with open(PATH_TEMPLATES) as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        filteredRecords = list(
            (filter(lambda x: x["technology"] == technology, data))
        )  # noqa: E501
        frameworks = list(map(lambda x: x["id"], filteredRecords))
        frameworksOptions = buildMenuOptions(frameworks)
        terminal_menu = TerminalMenu(
            frameworksOptions,
            title="Select a framework:",
            menu_cursor_style=MENU_CURSOR_STYLE,
            show_search_hint=SHOW_SEARCH_HINT,
        )
        idx = terminal_menu.show()
        selectedFramework = next(
            filter(lambda x: x["id"] == frameworks[idx], filteredRecords)
        )  # noqa: E501

        return (
            selectedFramework["id"],
            selectedFramework["gitRepository"],
            selectedFramework["profile"],
            selectedFramework["version"],
        )


def confirmSelection():
    options = buildMenuOptions(["Yes", "No"])
    terminal_menu = TerminalMenu(
        options, title="Do you want to confirm project initialization?"
    )  # noqa: E501
    menu_entry_index = terminal_menu.show()
    return scaffold() if menu_entry_index == 1 else True


def getOpenshiftRepositoryMetadata(projectName: str):
    # TODO: add rule to prevent camelcase and special characters
    # TODO: get those parameters in the stage generation
    gitRepository = getPrompt(
        f"Where will reside your code?", "https://www.github.com/user/repo.git"
    )
    gitCredentialsId = getPrompt(
        f"What's the git credential ID?", "gogs-repo-pw"
    )  # noqa: E501
    return (
        gitRepository,
        gitCredentialsId,
    )  # noqa: E501


def scaffold(proxy: str = None):
    scaffoldConfig = {}
    sessionUuid = createNewSessionId()

    prepareWorkspace(sessionUuid, proxy)

    scaffoldConfig["strategy"] = getStrategyVersions(sessionUuid)

    PATH_TEMPLATES = f"/tmp/{sessionUuid}/templates/latest.yml"
    technologySelected = getTechnology(PATH_TEMPLATES)
    scaffoldConfig["technology"] = technologySelected

    frameworkId, templateUri, profile, version = getFramework(
        PATH_TEMPLATES, technologySelected
    )
    scaffoldConfig["frameworkId"] = frameworkId
    scaffoldConfig["templateUri"] = templateUri
    scaffoldConfig["profile"] = profile
    scaffoldConfig["version"] = version

    scaffoldConfig["projectName"] = getPrompt("Select a project name:")

    # configure path project
    relativeProjectPath = getPrompt(
        "Where do you want to generate your project (local)?"
    )

    confirmSelection()

    PATH_PROJECT = (
        f"{removeTrailSlash(relativeProjectPath)}/{scaffoldConfig['projectName']}"
    )

    gitConfig = {"config": f"http.proxy={proxy}"} if proxy is not None else {}
    Repo.clone_from(f"{scaffoldConfig['templateUri']}", PATH_PROJECT, **gitConfig)

    shutil.rmtree(f"{PATH_PROJECT}/.git", ignore_errors=True)

    (
        gitRepository,
        gitCredentialsId,
    ) = getOpenshiftRepositoryMetadata(scaffoldConfig["projectName"])

    templateMeta = dict(scaffoldConfig)
    del templateMeta["projectName"]

    ocpeasyConfig = {
        "projectName": scaffoldConfig["projectName"],
        "gitRepository": gitRepository,
        "gitCredentialsId": gitCredentialsId,
        # TODO: add SHA template,
        "templateMeta": {**templateMeta},
        "stages": [],
    }

    with open(f"{PATH_PROJECT}/{OCPEASY_CONFIG_NAME}", "w") as f:
        yaml.dump(ocpeasyConfig, f)

    cleanWorkspace(sessionUuid)
