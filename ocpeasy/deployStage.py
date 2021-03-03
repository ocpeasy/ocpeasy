# import openshift as oc
from .ocUtils import applyStage
from os import environ, getenv, path
from .utils import buildStageAssets, removeTrailSlash
from .notify import missingStage, missingConfigurationFile
import yaml

from .constants import OCPEASY_CONFIG_NAME


def deployStage(stageId: str, proxy: str = None):
    buildStageAssets(stageId, proxy)
    PREFIX_PROJECT_ROOT = environ.get("PROJECT_DEV_PATH", ".")

    # TODO: define read ocpeasyConfig function
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
                applyStage(
                    stage.get("projectId"), f"{PREFIX_PROJECT_ROOT}/.ocpeasy/{stageId}"
                )
            else:
                return missingStage()
    else:
        return missingConfigurationFile()
