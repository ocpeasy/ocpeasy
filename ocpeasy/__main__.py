import fire
import sys
import os

PARENT_FOLDER = ".."
SCRIPT_DIR = os.path.dirname(
    os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__)))
)
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PARENT_FOLDER)))

from ocpeasy.scaffold import scaffold  # noqa E402, F401
from ocpeasy.createStage import createStage  # noqa E402, F401
from ocpeasy.deployStage import deployStage  # noqa E402, F401
from ocpeasy.destroyStage import destroyStage  # noqa E402, F401


def cli():
    sys.exit(fire.Fire())


if __name__ == "__main__":
    cli()
