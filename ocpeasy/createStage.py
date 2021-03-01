from os import path, getenv, mkdir
from .utils import (
    removeTrailSlash,
    createNewSessionId,
    cloneStrategyRepository,
    cleanWorkspace,
    getPrompt,
)
from .constants import OCPEASY_CONFIG_NAME, OCPEASY_CONTEXT_PATH
from .notify import missingConfigurationFile, stageCreated
import yaml


def createStage(proxy: str = None):
    projectDevPath = getenv("PROJECT_DEV_PATH", None)
    pathProject = "." if not projectDevPath else removeTrailSlash(projectDevPath)

    # check if ocpeasy config exists
    ocpPeasyConfigFound = False
    ocpPeasyConfigPath = f"{pathProject}/{OCPEASY_CONFIG_NAME}"

    if path.isfile(ocpPeasyConfigPath):
        ocpPeasyConfigFound = True
    else:
        missingConfigurationFile()
        return

    if ocpPeasyConfigFound:
        sessionId = createNewSessionId()
        deployConfigDict = dict()
        # will contain stage related metadata
        stageConfiguration = dict()
        with open(ocpPeasyConfigPath) as ocpPeasyConfigFile:
            deployConfigDict = yaml.load(ocpPeasyConfigFile, Loader=yaml.FullLoader)
            globalValues = dict(deployConfigDict)
            excludedKeys = ["templateMeta", "stages"]
            for excluded in excludedKeys:
                del globalValues[excluded]

            cloneStrategyRepository(sessionId, proxy)
            OCPEASY_DEPLOYMENT_PATH = f"{pathProject}/{OCPEASY_CONTEXT_PATH}"
            try:
                # shutil.rmtree(OCPEASY_DEPLOYMENT_PATH, ignore_errors=True)
                if not path.exists(OCPEASY_DEPLOYMENT_PATH):
                    mkdir(OCPEASY_DEPLOYMENT_PATH)

                # get from CLI (e.g.: --stage=dev) ?
                # TODO: check if stage already exists
                stageId = getPrompt(
                    f"What's the id of your stage (default: development)", "development"
                )

                similarStageId = list(
                    filter(
                        lambda x: (x.get("stageId") == stageId),
                        deployConfigDict["stages"],
                    )
                )
                if len(similarStageId) > 0:
                    print(
                        f"\nOpenShift stage ({stageId}) for project [{pathProject}] exists already \u274c"
                    )
                    return

                ocpProject = getPrompt(f"What's the name of the OpenShift project")
                # TODO: check if the container name already exists for the project
                containerId = getPrompt(
                    f"What's the OpenShift container ID/Name (unique per project)"
                )
                containerRoute = getPrompt(
                    f"What's the route of your application? [{containerId}-{ocpProject}.<hostOcp>]"
                )
                podReplicas = getPrompt(
                    f"What's the number of replicas required for your app?"
                )

                stageConfiguration["stageId"] = stageId
                stageConfiguration["ocpProject"] = ocpProject
                stageConfiguration["containerId"] = containerId
                stageConfiguration["containerRoute"] = containerRouter
                stageConfiguration["podReplicas"] = podReplicas
                stageConfiguration["modules"] = []
                stageConfiguration["dockerfile"] = "./Dockerfile"

            except OSError:
                print("Creation of the directory %s failed" % OCPEASY_CONTEXT_PATH)

            cleanWorkspace(sessionId)
            deployConfigDict = {
                **deployConfigDict,
                "stages": [*deployConfigDict["stages"], stageConfiguration],
            }

        with open(ocpPeasyConfigPath, "w") as ocpPeasyConfigFile:
            ocpPeasyConfigFile.write(yaml.dump(deployConfigDict))

    stageCreated(stageId, pathProject)
