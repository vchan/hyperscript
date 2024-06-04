from __future__ import annotations

import re
from html import escape
from typing import Any, Dict, List, Tuple, Union

TAG_PATTERN = re.compile(r"([.#]?[^\s#.]+)")
VOID_ELEMENTS = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "source",
    "track",
    "wbr",
}


class SafeStr(str):
    pass


class Element:
    __hash__ = object.__hash__

    def __init__(self, tag: str, *args: Any, autoescape: bool = True) -> None:
        self.tag, self.classes, self.id_selector = self.parse_tag(tag)
        self.autoescape = autoescape
        self.attrs, self.children = self.parse_args(args)

        if self.is_void and self.children:
            raise ValueError(f"{self.tag} is a void element and cannot have content")

    @property
    def is_void(self) -> bool:
        return self.tag in VOID_ELEMENTS

    def parse_tag(self, tag: str) -> Tuple[str, List[str], str]:
        """Parse the tag and extract classes and id.

        Hyperscript supports a shortcut for setting class and id if the tag
        name is of the form `name.class1.class2#id`. This function returns a
        tuple of three items: (tag, classes, id).
        """
        tag, *classes_and_id = re.findall(TAG_PATTERN, tag)
        classes = []
        id_selector = ""
        for item in classes_and_id:
            if item.startswith("."):
                classes.append(item[1:])
            elif item.startswith("#"):
                id_selector = item[1:]
        return tag, classes, id_selector

    def parse_args(self, args: tuple[Any]) -> Tuple[dict[str, Any], list[Any]]:
        attrs = {}
        children = []
        for arg in args:
            if isinstance(arg, dict):
                for key, value in arg.items():
                    if key == "style":
                        value = self.parse_style(value)
                    attrs[key] = value
            elif isinstance(arg, list):
                children.extend(arg)
            else:
                children.append(arg)
        return attrs, children

    def parse_style(self, style: Union[str, Dict[str, str]]) -> str:
        if isinstance(style, str):
            return style
        return "; ".join(f"{k}: {v}" for k, v in style.items())

    def _stringify(self, value: Any) -> str:
        if not isinstance(value, str):
            return str(value)
        elif self.autoescape and not isinstance(value, SafeStr):
            return escape(value)
        return value

    def __str__(self) -> str:
        opening_tags = [self.tag]
        if self.classes:
            classes = " ".join(self.classes)
            opening_tags.append(f'class="{classes}"')
        if self.id_selector:
            opening_tags.append(f'id="{self.id_selector}"')
        if self.attrs:
            attrs = []
            for attr, value in self.attrs.items():
                if value is True or value is None:
                    attrs.append(f"{attr}")
                else:
                    attrs.append(f'{attr}="{self._stringify(value)}"')
            opening_tags.extend(attrs)
        opening_tag = " ".join(opening_tags)
        if self.is_void:
            return f"<{opening_tag}>"
        children = "".join(self._stringify(child) for child in self.children)
        return f"<{opening_tag}>{children}</{self.tag}>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Element):
            return str(self) == str(other)
        if isinstance(other, str):
            return str(self) == other
        return False
