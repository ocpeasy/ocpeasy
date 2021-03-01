# import openshift as oc
from .ocUtils import applyStage
from os import environ
from .utils import buildStageAssets


def deploy(projectId: str, stageId: str):
    # print("OpenShift server version: {}".format(oc.get_server_version()))
    # generateYaml
    buildStageAssets(stageId)
    PREFIX_PROJECT_ROOT = environ.get("PROJECT_DEV_PATH", ".")
    applyStage(projectId, f"{PREFIX_PROJECT_ROOT}/.ocpeasy/{stageId}")

    # Set a project context for all inner `oc` invocations and limit execution to 10 minutes
    # with oc.project(projectId), oc.timeout(10 * 60):
    #     # Print the list of qualified pod names (e.g. ['pod/xyz', 'pod/abc', ...]  in the current project
    #     print(
    #         "Found the following pods in {}: {}".format(
    #             oc.get_project_name(), oc.selector("pods").qnames()
    #         )
    #     )

    # connect to OCP
    # TODO: check if the project has been initialized / ocpeasy.yml exists
    # TODO: check if the selected stage exists in the ocpeasy.yml file
    # (otherwise ask user if it should be created)
    # TODO: get oc path from environment variable, if not simply call `oc`
