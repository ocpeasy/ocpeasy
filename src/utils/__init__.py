from ..constants import ALPHABET_LIST_CHAR


def buildMenuOptions(arr):
    counter = 0
    options = []
    for el in arr:
        options.append(f"[{ALPHABET_LIST_CHAR[counter]}] {el}")
        counter += 1
    return options


def getPrompt(promptText: str, default=None, rule=None):
    value = ""
    while len(value) == 0:
        value = input(
            f"{promptText} {f'(default: {default})' if default != None else ''}"  # noqa: E501
        )
        if len(value) == 0 and default:
            value = default
    return value
