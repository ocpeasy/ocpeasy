from os import path, getenv, mkdir
from .utils import removeTrailSlash
from .constants import OCPEASY_CONFIG_NAME, OCPEASY_CONTEXT_PATH
import yaml


def buildStage(stageId: str):
    projectEnvPath = getenv("POETRY_DEV_PATH", None)
    pathProject = "." if not projectEnvPath else removeTrailSlash(projectEnvPath)

    ocpPeasyConfigFound = False
    ocpPeasyConfigPath = f"{pathProject}/{OCPEASY_CONFIG_NAME}"

    if path.isfile(ocpPeasyConfigPath):
        ocpPeasyConfigFound = True
    else:
        print("ocpeasy.yml file does not exist")

    if ocpPeasyConfigFound:
        # TODO: validate ocpeasy.yml file
        # TODO: open ocpeasy as dict
        with open(ocpPeasyConfigPath) as ocpPeasyConfigFile:
            deployConfigDict = yaml.load(ocpPeasyConfigFile, Loader=yaml.FullLoader)
            print(deployConfigDict)

            # ocpTemplateFiles = ["bc", "dc", "img", "route", "svc"]
            try:
                mkdir(f"{pathProject}/{OCPEASY_CONTEXT_PATH}")
            except OSError:
                print("Creation of the directory %s failed" % OCPEASY_CONTEXT_PATH)

    print(f"buildStage {stageId} {pathProject}")
