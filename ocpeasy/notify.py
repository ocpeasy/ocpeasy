ERROR_CHAR = "\u274c"
SUCCESS_CHAR = "\u2713"


def missingConfigurationFile():
    print(
        f"{ERROR_CHAR} nocpeasy.yml file does not exist, run `ocpeasy scaffold|init` first"
    )


def stageCreated(stageId: str, pathProject: str):
    print(
        f"{SUCCESS_CHAR} new OpenShift stage created ({stageId}) for project [{pathProject}]"
    )


def ocpeasyConfigFileUpdated():
    print(f"{SUCCESS_CHAR} ocpeasy.yml file refreshed")


def missingStage():
    print(f"{ERROR_CHAR} stage doesn't exist")


def ocpeasyStageAssetsGenerated():
    print(f"{SUCCESS_CHAR} OpenShift assets generated")


def ocBinaryMissingFromPath():
    print(f"{ERROR_CHAR} oc is not properly installed")
