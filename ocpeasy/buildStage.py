import os


def buildStage(stageId: str):
    devPath = os.getenv("POETRY_DEV_PATH", None)
    pathProject = "." if not devPath else devPath

    print(f"buildStage {stageId} {pathProject}")
