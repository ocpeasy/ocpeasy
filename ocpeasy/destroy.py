from os import path, getenv
from .utils import removeTrailSlash
from .constants import OCPEASY_CONFIG_NAME
from .notify import missingConfigurationFile, missingStage
import yaml

from .ocUtils import destroyApplication


def destroy(stageId: str):
    projectDevPath = getenv("PROJECT_DEV_PATH", None)
    pathProject = "." if not projectDevPath else removeTrailSlash(projectDevPath)
    ocpPeasyConfigPath = f"{pathProject}/{OCPEASY_CONFIG_NAME}"

    if path.isfile(ocpPeasyConfigPath):
        with open(ocpPeasyConfigPath) as ocpPeasyConfigFile:
            deployConfigDict = yaml.load(ocpPeasyConfigFile, Loader=yaml.FullLoader)
            globalValues = dict(deployConfigDict)
            stage = next(
                (x for x in globalValues.get("stages") if x.get("stageId") == stageId),
                None,
            )
            if stage:
                destroyApplication(stage.get("ocpProject"), stage.get("containerId"))
            else:
                return missingStage()
    else:
        return missingConfigurationFile()
