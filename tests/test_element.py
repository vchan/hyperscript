import unittest

from hyperscript import h


class TestElement(unittest.TestCase):
    def test_element(self):
        self.assertEqual(str(h("div")), "<div></div>")

    def test_nested(self):
        self.assertEqual(
            str(h("div", h("h1", "Header"), h("p", "Paragraph"))),
            "<div><h1>Header</h1><p>Paragraph</p></div>",
        )

    def test_nested_arrays(self):
        self.assertEqual(
            str(h("div", [h("h1", "Header"), h("p", "Paragraph")])),
            "<div><h1>Header</h1><p>Paragraph</p></div>",
        )

    def test_namespace(self):
        self.assertEqual(str(h("myns:mytag")), "<myns:mytag></myns:mytag>")

    def test_id_selector(self):
        self.assertEqual(str(h("div#foo")), '<div id="foo"></div>')

    def test_class_selector(self):
        self.assertEqual(str(h("div.foo")), '<div class="foo"></div>')
        self.assertEqual(str(h("div.foo.bar")), '<div class="foo bar"></div>')

    def test_properties(self):
        self.assertEqual(
            str(h("a", {"href": "https://example.com/"})),
            '<a href="https://example.com/"></a>',
        )
        self.assertEqual(str(h("div.foo.bar")), '<div class="foo bar"></div>')

        self.assertEqual(str(h("div", {"prop": "foo"})), '<div prop="foo"></div>')

        self.assertEqual(
            str(h("button", {"disabled": None})), "<button disabled></button>"
        )

        self.assertEqual(
            str(h("button", {"disabled": True})), "<button disabled></button>"
        )

        self.assertEqual(
            str(h("button", {"disabled": ""})), '<button disabled=""></button>'
        )

    def test_styles(self):
        self.assertEqual(
            str(h("div", {"style": {"color": "red"}})), '<div style="color: red"></div>'
        )

    def test_str_styles(self):
        self.assertEqual(
            str(h("div", {"style": "color: red"})), '<div style="color: red"></div>'
        )

    def test_other_types(self):
        self.assertEqual(str(h("div", True, 5, None)), "<div>True5None</div>")

    def test_void(self):
        self.assertEqual(str(h("br")), "<br>")

        with self.assertRaises(ValueError):
            h("br", "foo")
