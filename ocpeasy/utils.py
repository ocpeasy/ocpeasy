from .constants import (
    ALPHABET_LIST_CHAR,
    EMPTY_STRING,
    BASE_STRATEGIES_REPOSITORY,
    OCPEASY_CONFIG_NAME,
    OCPEASY_CONTEXT_PATH,
    CLI_NAME,
)

from uuid import uuid4
from git import Repo
import shutil
import yaml

from os import getenv, path, walk, mkdir

from .notify import missingConfigurationFile, ocpeasyStageAssetsGenerated

from .__version__ import __version__


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
    kwargs = {"config": f"http.proxy={proxy}"} if proxy is not None else {}
    Repo.clone_from(f"{BASE_STRATEGIES_REPOSITORY}", PATH_SESSION, **kwargs)


def cleanWorkspace(sessionId: str):
    shutil.rmtree(f"/tmp/{sessionId}", ignore_errors=True)


def replaceAll(text: str, dic: dict):
    for i in dic.keys():
        text = text.replace(f"{i}", dic.get(i))
    return text.replace("[", "").replace("]", "")


def buildStageAssets(stageId: str, proxy: str):
    projectDevPath = getenv("PROJECT_DEV_PATH", None)
    pathProject = "." if not projectDevPath else removeTrailSlash(projectDevPath)

    # check if ocpeasy config exists
    ocpPeasyConfigFound = False
    ocpPeasyConfigPath = f"{pathProject}/{OCPEASY_CONFIG_NAME}"

    if path.isfile(ocpPeasyConfigPath):
        ocpPeasyConfigFound = True
    else:
        return missingConfigurationFile()

    if ocpPeasyConfigFound:
        sessionId = createNewSessionId()
        deployConfigDict = dict()
        # will contain stage related metadata
        stageConfiguration = dict()
        # will contain token to be replaced into yml config
        tokenConfiguration = dict()
        # TODO: validate ocpeasy.yml file

        cloneStrategyRepository(sessionId, proxy)
        OCPEASY_DEPLOYMENT_PATH = f"{pathProject}/{OCPEASY_CONTEXT_PATH}"

        with open(ocpPeasyConfigPath) as ocpPeasyConfigFile:
            deployConfigDict = dict(
                yaml.load(ocpPeasyConfigFile, Loader=yaml.FullLoader)
            )
            # TODO: get stage corresponding to stageId

            selectedStages = list(
                filter(
                    lambda x: (x.get("stageId") == stageId),
                    deployConfigDict["stages"],
                )
            )

            stageConfiguration = selectedStages[0]

            excludedKeys = ["stageId", "modules"]
            for excluded in excludedKeys:
                del stageConfiguration[excluded]

            tokenConfiguration = {
                **stageConfiguration,
                "generatedBy": f"{CLI_NAME} {__version__}",
            }

            strategyId = deployConfigDict["templateMeta"]["strategy"]
            OCP_PROFILE_PATH = f"/tmp/{sessionId}/{strategyId}/profiles/{deployConfigDict['templateMeta']['profile']}"
            _, _, configFiles = next(walk(OCP_PROFILE_PATH))

            # sample: configFiles = ['bc.yaml', 'svc.yaml', 'dc.yaml', 'route.yaml', 'img.yaml']
            STAGE_CONFIG_ROOT = f"{OCPEASY_DEPLOYMENT_PATH}/{stageId}"

            # will ensure new assets are generated each time
            if path.exists(STAGE_CONFIG_ROOT):
                shutil.rmtree(STAGE_CONFIG_ROOT)

            mkdir(STAGE_CONFIG_ROOT)

            for configFile in configFiles:
                configurationPath = f"{OCP_PROFILE_PATH}/{configFile}"
                with open(configurationPath) as f:
                    configAsDict = yaml.load(f, Loader=yaml.FullLoader)
                    ocpContextYaml = yaml.dump(configAsDict)
                    ocpContextBuild = replaceAll(ocpContextYaml, tokenConfiguration)
                    # generate yaml files in .ocpeasy/{stage}/{configFile}
                    print(ocpContextBuild)
                    stageConfigFile = f"{STAGE_CONFIG_ROOT}/{configFile}"
                    with open(stageConfigFile, "w") as configTarget:
                        configTarget.write(ocpContextBuild)

            cleanWorkspace(sessionId)

        return ocpeasyStageAssetsGenerated()
