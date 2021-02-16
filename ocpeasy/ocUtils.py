import logging
import sh
from sh import ErrorReturnCode

log = logging.getLogger(__name__)

def runOc(*args, **kwargs):
    return sh.oc(*args, **kwargs, _tee=True)

def applyStage(project, stagePath):
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