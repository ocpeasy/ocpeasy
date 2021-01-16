from os import path, getenv
from .utils import removeTrailSlash


def buildStage(stageId: str):
    projectPath = getenv("POETRY_DEV_PATH", None)
    pathProject = "." if not projectPath else projectPath

    ocpPeasyConfigFound = False

    # TODO: check if ocpeasy.yml file exists
    if path.isfile(f"{removeTrailSlash(pathProject)}/ocpeasy.yml"):
        ocpPeasyConfigFound = True
    else:
        print("ocpeasy.yml file does not exist")

    if ocpPeasyConfigFound:
        print("ocpeasy exists")

    print(f"buildStage {stageId} {pathProject}")
