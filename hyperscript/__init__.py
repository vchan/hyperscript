from __future__ import annotations

from typing import Any, Optional

from hyperscript.element import Element, SafeStr

AUTOESCAPE = True


def h(
    tag: str, *args: Any, autoescape: Optional[bool] = None, remove_empty: bool = False
) -> Element:
    if autoescape is None:
        autoescape = AUTOESCAPE
    return Element(tag, *args, autoescape=autoescape, remove_empty=remove_empty)


def safe(value: str) -> SafeStr:
    if not isinstance(value, str):
        raise TypeError(f"expected a str, got {type(value)}")
    return SafeStr(value)
