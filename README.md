# Hyperscript
Hyperscript is a lightweight library that allows you to write HTML with Python. It is heavily inspired by [HyperScript](https://github.com/hyperhype/hyperscript).

## Example usage
```
>>> print(h("p", "Hello world!"))
<p>Hello world!</p>
```
Class and id selectors
```
>>> print(h("p.class1#id", "Hello world!"))
<p class="class1" id="id">Hello world!</p>
```
Style
```
>>> print(h("p", "Hello world!", {"style": {"color": "red"}}))
<p style="color: red">Hello world!</p>
```
Nesting elements
```
>>> print(h("div", h("p", "Hello world!")))
<div><p>Hello world!</p></div>
```
Attributes
```
>>> print(h("a", {"href": "https://www.example.com"}, "link"))
<a href="https://www.example.com">link</a>
```
Boolean attributes
```
>>> print(h("input", {"type": "checkbox", "checked": True}))  # Behavior is the same if "checked" is None
<input type="checkbox" checked>
>>> print(h("input", {"type": "checkbox", "checked": ""}))
<input type="checkbox" checked="">
>>> print(h("input", {"type": "checkbox", "checked": False}))
<input type="checkbox">
```
