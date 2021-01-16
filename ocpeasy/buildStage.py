from os import path, getenv
from .utils import removeTrailSlash
from .constants import OCPEASY_CONFIG_NAME


def buildStage(stageId: str):
    projectPath = getenv("POETRY_DEV_PATH", None)
    pathProject = "." if not projectPath else projectPath

    ocpPeasyConfigFound = False
    ocpPeasyConfigPath = f"{removeTrailSlash(pathProject)}/{OCPEASY_CONFIG_NAME}"

    # TODO: check if ocpeasy.yml file exists
    if path.isfile(ocpPeasyConfigPath):
        ocpPeasyConfigFound = True
    else:
        print("ocpeasy.yml file does not exist")

    if ocpPeasyConfigFound:
        print("ocpeasy exists")

    print(f"buildStage {stageId} {pathProject}")
