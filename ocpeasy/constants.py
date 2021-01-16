from string import ascii_lowercase

PLATFORM_LABEL = "Red Hat OpenShift®"

GIT_PROVIDER = "github.com"
CLI_NAME = "ocpeasy"
GIT_DEPLOY_REPO_NAME = f"{CLI_NAME}-deploy-strategies"
BASE_STRATEGIES_REPOSITORY = (
    f"https://{GIT_PROVIDER}/{CLI_NAME}/{GIT_DEPLOY_REPO_NAME}"  # noqa: E501
)
PREFIX_STRATEGY = "openshift_"

ALPHABET_LIST_CHAR = list(ascii_lowercase)

# CLI_OPTIONS
MENU_CURSOR_STYLE = ("fg_green", "bold")
SHOW_SEARCH_HINT = True

OCPEASY_CONFIG_NAME = f"{CLI_NAME}.yml"
OCPEASY_CONTEXT_PATH = f".{CLI_NAME}"
# MISC
EMPTY_STRING = ""
