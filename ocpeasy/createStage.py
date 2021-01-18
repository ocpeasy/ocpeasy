from os import path, getenv, mkdir, walk
from .utils import (
    removeTrailSlash,
    createNewSessionId,
    cloneStrategyRepository,
    cleanWorkspace,
    getPrompt,
    replaceAll,
)
from .constants import OCPEASY_CONFIG_NAME, OCPEASY_CONTEXT_PATH, CLI_NAME
import yaml

from .__version__ import __version__


def createStage():
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

            cloneStrategyRepository(sessionId)
            OCPEASY_DEPLOYMENT_PATH = f"{pathProject}/{OCPEASY_CONTEXT_PATH}"
            try:
                # shutil.rmtree(OCPEASY_DEPLOYMENT_PATH, ignore_errors=True)
                if not path.exists(OCPEASY_DEPLOYMENT_PATH):
                    mkdir(OCPEASY_DEPLOYMENT_PATH)

                stageConfiguration = tokenConfiguration = {}

                # get from CLI (e.g.: --stage=dev) ?
                # TODO: check if stage already exists
                stageId = getPrompt(
                    f"What's the id of your stage (default: development)", "development"
                )
                ocpProject = getPrompt(f"What's the name of the OpenShift project")
                # TODO: check if the container name already exists for the project
                containerId = getPrompt(
                    f"What's the OpenShift container ID/Name (unique per project)"
                )
                containerRouter = getPrompt(
                    f"What's the route of your application? (http(?s)://{containerId}-{ocpProject}.<hostOcp>)"
                )
                podReplicas = getPrompt(
                    f"What's the number of replicas required for your app?"
                )

                stageConfiguration["stageId"] = stageId
                stageConfiguration["ocpProject"] = ocpProject
                stageConfiguration["containerId"] = containerId
                stageConfiguration["containerRouter"] = containerRouter
                stageConfiguration["podReplicas"] = podReplicas

                tokenConfiguration["ocpProject"] = ocpProject
                tokenConfiguration["containerId"] = containerId
                tokenConfiguration["containerRouter"] = containerRouter
                tokenConfiguration["podReplicas"] = podReplicas
                tokenConfiguration["generatedBy"] = f"{CLI_NAME} CLI ({__version__})"
                tokenConfiguration["gitRepository"] = globalValues["gitRepository"]
                tokenConfiguration["gitCredentialsId"] = globalValues[
                    "gitCredentialsId"
                ]

                strategyId = deployConfigDict["templateMeta"]["strategy"]
                OCP_PROFILE_PATH = f"/tmp/{sessionId}/{strategyId}/profiles/{deployConfigDict['templateMeta']['profile']}"
                _, _, configFiles = next(walk(OCP_PROFILE_PATH))
                # sample: configFiles = ['bc.yaml', 'svc.yaml', 'dc.yaml', 'route.yaml', 'img.yaml']
                STAGE_CONFIG_ROOT = f"{OCPEASY_DEPLOYMENT_PATH}/{stageId}"
                if not path.exists(STAGE_CONFIG_ROOT):
                    mkdir(STAGE_CONFIG_ROOT)

                for configFile in configFiles:
                    configurationPath = f"{OCP_PROFILE_PATH}/{configFile}"
                    with open(configurationPath) as f:
                        configAsDict = yaml.load(f, Loader=yaml.FullLoader)
                        ocpContextYaml = yaml.dump(configAsDict)
                        ocpContextBuild = replaceAll(ocpContextYaml, tokenConfiguration)
                        # generate yaml files in .ocpeasy/stage/{configFile}
                        stageConfigFile = f"{STAGE_CONFIG_ROOT}/{configFile}"
                        with open(stageConfigFile, "w") as configTarget:
                            configTarget.write(ocpContextBuild)

            except OSError:
                print("Creation of the directory %s failed" % OCPEASY_CONTEXT_PATH)

            cleanWorkspace(sessionId)

    print(
        f"\n\nnew OpenShift stage created ({stageId}) for project [{pathProject}] \u2713"
    )
