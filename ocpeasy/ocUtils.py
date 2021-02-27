import logging
import sh
from sh import ErrorReturnCode

log = logging.getLogger(__name__)


def runOc(*args, **kwargs):
    return sh.oc(*args, **kwargs, _tee=True)


def applyStage(project: str, stagePath: str):
    getProject(project)
    try:
        runOc("apply", "-f", stagePath)
    except ErrorReturnCode as err:
        log.error(err)


def getProject(projectId):
    try:
        runOc("project", projectId)
    except ErrorReturnCode:
        log.error(f"Unable to get {projectId}")


def destroyApplication(project: str, applicationId: str):
    getProject(project)
    try:
        runOc("delete", "all", '--selector', f"app={applicationId}")
        runOc("delete", "bc", applicationId)
        runOc("delete", "dc", applicationId)
    except ErrorReturnCode:
        log.error(f"Unable to get {projectId}")
