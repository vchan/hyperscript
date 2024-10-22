import types
import unittest

from hyperscript import h, safe


class TestElement(unittest.TestCase):
    def test_element(self) -> None:
        self.assertEqual(str(h("div")), "<div></div>")

    def test_nested(self) -> None:
        self.assertEqual(
            str(h("div", h("h1", "Header"), h("p", "Paragraph"))),
            "<div><h1>Header</h1><p>Paragraph</p></div>",
        )

    def test_nested_arrays(self) -> None:
        self.assertEqual(
            str(h("div", [h("h1", "Header"), h("p", "Paragraph")])),
            "<div><h1>Header</h1><p>Paragraph</p></div>",
        )

    def test_namespace(self) -> None:
        self.assertEqual(str(h("myns:mytag")), "<myns:mytag></myns:mytag>")

    def test_id_selector(self) -> None:
        self.assertEqual(str(h("div#foo")), '<div id="foo"></div>')

    def test_class_selector(self) -> None:
        self.assertEqual(str(h("div.foo")), '<div class="foo"></div>')
        self.assertEqual(str(h("div.foo.bar")), '<div class="foo bar"></div>')

    def test_attributes(self) -> None:
        self.assertEqual(
            str(h("a", {"href": "https://example.com/"})),
            '<a href="https://example.com/"></a>',
        )
        self.assertEqual(str(h("div.foo.bar")), '<div class="foo bar"></div>')

        self.assertEqual(str(h("div", {"prop": "foo"})), '<div prop="foo"></div>')

        self.assertEqual(
            str(h("div", types.MappingProxyType({"prop": "foo"}))),
            '<div prop="foo"></div>',
        )

        self.assertEqual(
            str(h("button", {"disabled": None})), "<button disabled></button>"
        )

        self.assertEqual(
            str(h("button", {"disabled": True})), "<button disabled></button>"
        )

        self.assertEqual(
            str(h("button", {"disabled": ""})), '<button disabled=""></button>'
        )

        self.assertEqual(str(h("button", {"disabled": False})), "<button></button>")

    def test_styles(self) -> None:
        self.assertEqual(
            str(h("div", {"style": {"color": "red"}})), '<div style="color: red"></div>'
        )

    def test_str_styles(self) -> None:
        self.assertEqual(
            str(h("div", {"style": "color: red"})), '<div style="color: red"></div>'
        )

    def test_other_types(self) -> None:
        self.assertEqual(
            str(h("div", True, 5, False, None, "")), "<div>True5False</div>"
        )

    def test_void(self) -> None:
        self.assertEqual(str(h("br")), "<br>")

        with self.assertRaises(ValueError):
            h("br", "foo")

    def test_equality(self) -> None:
        self.assertEqual(h("div"), h("div"))

        self.assertEqual(h("div", h("p", "Foo")), h("div", h("p", "Foo")))

        self.assertEqual(h("div", h("p", "Foo")), "<div><p>Foo</p></div>")

        self.assertNotEqual(h("div"), h("p"))

        self.assertNotEqual(h("div", h("p", "Foo")), h("div", h("p", "Bar")))

    def test_escape(self) -> None:
        self.assertEqual(str(h("div", "<&>", autoescape=False)), "<div><&></div>")

        self.assertEqual(str(h("div", "<&>")), "<div>&lt;&amp;&gt;</div>")

        self.assertEqual(
            str(h("div", {"prop": "<&>"})),
            '<div prop="&lt;&amp;&gt;"></div>',
        )

    def test_safe(self) -> None:
        self.assertEqual(str(h("div", safe("<&>"))), "<div><&></div>")

        self.assertEqual(
            str(h("div", {"prop": safe("<&>")})),
            '<div prop="<&>"></div>',
        )

        with self.assertRaises(TypeError):
            safe(h("div"))  # type: ignore

    def test_empty(self) -> None:
        self.assertEqual(str(h("div")), "<div></div>")
        self.assertEqual(str(h("div", None)), "<div></div>")
        self.assertEqual(str(h("div", "")), "<div></div>")
        self.assertEqual(str(h("div", "", None)), "<div></div>")

    def test_remove_empty(self) -> None:
        self.assertEqual(
            str(
                h(
                    "div",
                    h("div"),
                    "foo",
                    h("div", "bar"),
                    h("div", ""),
                    remove_empty=False,
                )
            ),
            "<div><div></div>foo<div>bar</div><div></div></div>",
        )
        self.assertEqual(
            str(
                h(
                    "div",
                    h("div"),
                    "foo",
                    h("div", "bar"),
                    h("div", ""),
                    remove_empty=True,
                )
            ),
            "<div>foo<div>bar</div></div>",
        )

        self.assertEqual(str(h("div", h("br"), remove_empty=True)), "<div><br></div>")

        self.assertEqual(
            str(
                h(
                    "div",
                    h(
                        "div",
                        h("div", remove_empty=True),
                        remove_empty=True,
                    ),
                    remove_empty=True,
                )
            ),
            "",
        )
