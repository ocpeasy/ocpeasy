def missingConfigurationFile():
    print(f"\u274c nocpeasy.yml file does not exist, run `ocpeasy scaffold|init` first")


def stageCreated(stageId: str, pathProject: str):
    print(f"\u2713 new OpenShift stage created ({stageId}) for project [{pathProject}]")


def ocpeasyConfigFileUpdated():
    print(f"\u2713 ocpeasy.yml file refreshed")


def missingStage():
    print(f"\u274c stage doesn't exist")


def ocpeasyStageAssetsGenerated():
    print(f"\u2713 OpenShift assets generated")
