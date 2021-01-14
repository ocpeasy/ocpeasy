from . import buildMenuOptions


def test_buildMenuOptions():
    assert buildMenuOptions(["A", "B"]) == ["[a] A", "[b] B"]
