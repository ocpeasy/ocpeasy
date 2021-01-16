from os import path, getenv, mkdir
from .utils import (
    removeTrailSlash,
    createNewSessionId,
    cloneStrategyRepository,
    cleanWorkspace,
)
from .constants import (
    OCPEASY_CONFIG_NAME,
    OCPEASY_CONTEXT_PATH,
)
import yaml
import shutil


def buildStage(stageId: str):
    projectEnvPath = getenv("POETRY_DEV_PATH", None)
    pathProject = "." if not projectEnvPath else removeTrailSlash(projectEnvPath)

    # check if ocpeasy config exists
    ocpPeasyConfigFound = False
    ocpPeasyConfigPath = f"{pathProject}/{OCPEASY_CONFIG_NAME}"

    if path.isfile(ocpPeasyConfigPath):
        ocpPeasyConfigFound = True
    else:
        print("ocpeasy.yml file does not exist")

    if ocpPeasyConfigFound:
        sessionId = createNewSessionId()
        # TODO: validate ocpeasy.yml file
        # TODO: open ocpeasy as dict
        with open(ocpPeasyConfigPath) as ocpPeasyConfigFile:
            deployConfigDict = yaml.load(ocpPeasyConfigFile, Loader=yaml.FullLoader)
            globalValues = dict(deployConfigDict)
            excludedKeys = ["templateMeta"]
            for excluded in excludedKeys:
                del globalValues[excluded]

            print(globalValues.keys())
            cloneStrategyRepository(sessionId)
            cleanWorkspace(sessionId)

            # ocpTemplateFiles = ["bc", "dc", "img", "route", "svc"]

            OCPEASY_DEPLOYMENT_PATH = f"{pathProject}/{OCPEASY_CONTEXT_PATH}"
            try:
                shutil.rmtree(OCPEASY_DEPLOYMENT_PATH, ignore_errors=True)
                mkdir(OCPEASY_DEPLOYMENT_PATH)
            except OSError:
                print("Creation of the directory %s failed" % OCPEASY_CONTEXT_PATH)

    print(f"buildStage {stageId} {pathProject}")
