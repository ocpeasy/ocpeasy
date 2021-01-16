from os import path, getenv, mkdir, walk
from .utils import (
    removeTrailSlash,
    createNewSessionId,
    cloneStrategyRepository,
    cleanWorkspace,
    getPrompt,
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

            # ocpTemplateFiles = ["bc", "dc", "img", "route", "svc"]
            # get configuration corresponding to the base app
            # f"/tmp/{sessionId}/{strategy}/profiles/{deployConfigDict['profile']}"
            print(deployConfigDict)

            OCPEASY_DEPLOYMENT_PATH = f"{pathProject}/{OCPEASY_CONTEXT_PATH}"
            try:
                shutil.rmtree(OCPEASY_DEPLOYMENT_PATH, ignore_errors=True)
                mkdir(OCPEASY_DEPLOYMENT_PATH)

                stageConfiguration = {}

                # TODO: check stageId doesnt exist
                # get stageId
                # get openshift project name (ocpProjectName)
                # get openshift container id (containerId)
                # configure openshift route (openshiftRoute)
                stageId = getPrompt(
                    f"What's the id of your stage (default: development)", "development"
                )
                ocpProjectName = getPrompt(f"What's the name of the OpenShift project")
                containerId = getPrompt(
                    f"What's the OpenShift container ID/Name (unique per project)"
                )
                containerRouter = getPrompt(
                    f"What's the route of your application? (http(?s)://{containerId}-{ocpProjectName}.<hostOcp>)"
                )
                podReplicas = getPrompt(
                    f"What's the number of replicas required for your app?"
                )

                stageConfiguration["stageId"] = stageId
                stageConfiguration["ocpProjectName"] = ocpProjectName
                stageConfiguration["containerId"] = containerId
                stageConfiguration["containerRouter"] = containerRouter
                stageConfiguration["podReplicas"] = podReplicas

                print(stageConfiguration)
                # TODO: append stage configuration to ocpeasy.yml

                # loop into config from
                print(deployConfigDict.get("templateMeta"))

                strategyId = deployConfigDict["templateMeta"]["strategy"]

                OCP_PROFILE_PATH = f"/tmp/{sessionId}/{strategyId}/profiles/{deployConfigDict['templateMeta']['profile']}"
                _, _, configFiles = next(walk(OCP_PROFILE_PATH))
                # configFiles = ['bc.yaml', 'svc.yaml', 'dc.yaml', 'route.yaml', 'img.yaml']
                for configFile in configFiles:
                    configurationPath = f"{OCP_PROFILE_PATH}/{configFile}"
                    with open(configurationPath) as f:
                        configAsDict = yaml.load(f, Loader=yaml.FullLoader)
                        print(configAsDict)

            except OSError:
                print("Creation of the directory %s failed" % OCPEASY_CONTEXT_PATH)

            cleanWorkspace(sessionId)

    print(f"buildStage {stageId} {pathProject}")
