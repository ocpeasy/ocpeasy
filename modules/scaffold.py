from git import Repo
import uuid
import shutil
from os import walk
from simple_term_menu import TerminalMenu
import string

alphabetList = list(string.ascii_lowercase)

def getStrategyVersions(sessionUuid: str):
    PATH_SESSION = f'/tmp/{sessionUuid}'
    Repo.clone_from("https://github.com/ocpeasy/ocpeasy-deploy-strategies.git", PATH_SESSION)
    _, folders, _ = next(walk(PATH_SESSION))
    strategies = list(filter(lambda x: x.startswith('openshift_'), folders))
    strategyOptions = []
    counter = 0

    for el in strategies:
        tmpStrategyString = el.replace('openshift_', '').replace('_', '.')
        strategyOptions.append(f'[{alphabetList[counter]}] Red Hat OpenShift {tmpStrategyString}')
        counter += 1
    
    terminal_menu = TerminalMenu(strategyOptions, title="Select an OpenShift strategy:")
    menu_entry_index = terminal_menu.show()
    print (f'[{strategies[menu_entry_index]}] selected')
    return strategies[menu_entry_index]

def getProgrammingLanguage():
    technologies = ["[a] TypeScript", "[b] Python", "[c] Rust"]
    terminal_menu = TerminalMenu(technologies, title="Select a technology")
    menu_entry_index = terminal_menu.show()
    print (f'[{technologies[menu_entry_index]}] selected')
    return technologies[menu_entry_index]

def getFrameworkTechnology():
    technologies = ["[a] NextJS", "[b] NestJS", "[c] Express"]
    terminal_menu = TerminalMenu(technologies, title="Select a framework")
    menu_entry_index = terminal_menu.show()
    print (f'[{technologies[menu_entry_index]}] selected')
    return technologies[menu_entry_index]

def confirmSelection():
    options = ["[a] Yes", "[b] No"]
    terminal_menu = TerminalMenu(options, title="Are you happy with your selection?")
    menu_entry_index = terminal_menu.show()
    print (f'[{options[menu_entry_index]}] selected')
    return options[menu_entry_index]

def cleanWorkspace(sessionUuid: str):
    shutil.rmtree(f'/tmp/{sessionUuid}', ignore_errors=True)


def scaffold():
    sessionUuid = uuid.uuid4().hex
    getStrategyVersions(sessionUuid)
    getProgrammingLanguage()
    getFrameworkTechnology()
    confirmSelection()
    cleanWorkspace(sessionUuid)