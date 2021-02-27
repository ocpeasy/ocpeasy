from .ocUtils import destroyApplication
from os import environ

PREFIX_PROJECT_ROOT = environ.get("PROJECT_DEV_PATH", ".")

def destroy(stageId: str):
    # TODO: read ocpeasy file
    # get corresponding stage
    # destroyApplication(stageId.get('project'), stageId.get('applicationId'))
    pass