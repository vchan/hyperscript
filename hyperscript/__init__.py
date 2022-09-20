from hyperscript.element import Element

__version__ = "0.0.1"


# pylint: disable=invalid-name
def h(tag: str, *args):
    return Element(tag, *args)
