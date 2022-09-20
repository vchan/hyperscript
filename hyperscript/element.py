import re
from typing import Dict, List, Tuple, Union

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


class Element:
    def __init__(self, tag, *args):
        self.tag, self.classes, self.id_selector = self.parse_tag(tag)
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

    def parse_args(self, args: list) -> Tuple[dict, list]:
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

    def __str__(self) -> str:
        opening_tag = [self.tag]
        if self.classes:
            classes = " ".join(self.classes)
            opening_tag.append(f'class="{classes}"')
        if self.id_selector:
            opening_tag.append(f'id="{self.id_selector}"')
        if self.attrs:
            attrs = []
            for attr, value in self.attrs.items():
                if value is True or value is None:
                    attrs.append(f"{attr}")
                else:
                    attrs.append(f'{attr}="{value}"')
            opening_tag.extend(attrs)
        opening_tag = " ".join(opening_tag)
        if self.is_void:
            return f"<{opening_tag}>"
        children = "".join(str(child) for child in self.children)
        return f"<{opening_tag}>{children}</{self.tag}>"
