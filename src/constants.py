from string import ascii_lowercase

GIT_PROVIDER = "github.com"
CLI_NAME = "ocpeasy"
GIT_DEPLOY_REPO_NAME = f"{CLI_NAME}-deploy-strategies"
BASE_STRATEGIES_REPOSITORY = f"https://{GIT_PROVIDER}/{CLI_NAME}/{GIT_DEPLOY_REPO_NAME}"
PREFIX_STRATEGY = "openshift_"

ALPHABET_LIST_CHAR = list(ascii_lowercase)

# CLI_OPTIONS
MENU_CURSOR_STYLE = ("fg_green", "bold")
SHOW_SEARCH_HINT = True
