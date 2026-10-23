import numpy as np

class HTMLTag:
    def __init__(self, tag_name, children=None, **attrs):
        self.tag_name = tag_name
        self.children = children if children is not None else []
        self.attrs = attrs

    def __repr__(self):
        attrs_str = "".join([f' {k}="{v}"' for k, v in self.attrs.items() if v is not None])
        children_str = "".join([str(c) for c in self.children])
        return f"<{self.tag_name}{attrs_str}>{children_str}</{self.tag_name}>"

def div(*args, **kwargs):
    return HTMLTag("div", children=list(args), **kwargs)

def a(*args, **kwargs):
    return HTMLTag("a", children=list(args), **kwargs)

def tagAppendAttributes(tag, **attrs):
    # If .cssSelector is provided, we look for children matching that tag name
    if ".cssSelector" in attrs:
        selector = attrs.pop(".cssSelector")
        for child in tag.children:
            if isinstance(child, HTMLTag) and child.tag_name == selector:
                for k, v in attrs.items():
                    if v is None:
                        child.attrs.pop(k, None)
                    else:
                        child.attrs[k] = v
    else:
        for k, v in attrs.items():
            if v is None:
                tag.attrs.pop(k, None)
            else:
                tag.attrs[k] = v
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attrs

def tagGetAttribute(tag, attr):
    return tag.attrs.get(attr)

# R: html <- div(a())
# r2py:entity:html
html = div(a())

# R: tagAppendAttributes(html, class = "foo")
# r2py:entity:tagAppendAttributes
tagAppendAttributes(html, class_="foo")

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
# r2py:entity:tagAppendAttributes_1
tagAppendAttributes(html, _cssSelector="a", class_="bar")

# R: tagAppendAttributes(html, contenteditable = NA)
# r2py:entity:tagAppendAttributes_2
tagAppendAttributes(html, contenteditable=None)

# R: tagHasAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagHasAttribute
tagHasAttribute_res = tagHasAttribute(div(foo="bar"), "foo")

# R: tagGetAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagGetAttribute
tagGetAttribute_res = tagGetAttribute(div(foo="bar"), "foo")