from typing import Any, Optional

from hyperscript.element import Element, Unescaped

__version__ = "0.0.3"

AUTOESCAPE = False


def h(tag: str, *args: Any, autoescape: Optional[bool] = None) -> Element:
    if autoescape is None:
        autoescape = AUTOESCAPE
    return Element(tag, *args, autoescape=autoescape)


def unescape(value: str) -> Unescaped:
    if not isinstance(value, str):
        raise TypeError(f"expected a str, got {type(value)}")
    return Unescaped(value)
