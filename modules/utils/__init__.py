from string import ascii_lowercase
from ..constants import ALPHABET_LIST_CHAR

def buildMenuOptions(arr):
    counter = 0
    options = []
    for el in arr:
        options.append(f"[{ALPHABET_LIST_CHAR[counter]}] {el}")
        counter += 1
    return options