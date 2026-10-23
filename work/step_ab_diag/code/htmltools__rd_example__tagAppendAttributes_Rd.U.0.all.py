import numpy as np

# Mocking htmltools behavior since there is no direct 1:1 equivalent 
# in Python that supports the specific attribute manipulation API of R's htmltools.
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
    children = [arg for arg in args]
    return HTMLTag("div", children=children, **kwargs)

def a(*args, **kwargs):
    children = [arg for arg in args]
    return HTMLTag("a", children=children, **kwargs)

def tagAppendAttributes(tag, **attrs):
    # If .cssSelector is provided, target the child
    if ".cssSelector" in attrs:
        selector = attrs.pop(".cssSelector")
        for child in tag.children:
            if isinstance(child, HTMLTag) and child.tag_name == selector:
                for k, v in attrs.items():
                    if v is np.nan or v is None:
                        child.attrs.pop(k, None)
                    else:
                        child.attrs[k] = v
        return tag
    
    # Otherwise apply to the tag itself
    for k, v in attrs.items():
        if v is np.nan or v is None:
            tag.attrs.pop(k, None)
        else:
            tag.attrs[k] = v
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attrs

def tagGetAttribute(tag, attr):
    return tag.attrs.get(attr)

# R: html <- div(a())
html = div(a())

# R: tagAppendAttributes(html, class = "foo")
tagAppendAttributes(html, class_="foo") # Using class_ because class is keyword

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
tagAppendAttributes(html, _cssSelector="a", class_="bar")

# R: tagAppendAttributes(html, contenteditable = NA)
tagAppendAttributes(html, contenteditable=np.nan)

# R: tagHasAttribute(div(foo = "bar"), "foo")
tagHasAttribute(div(foo="bar"), "foo")

# R: tagGetAttribute(div(foo = "bar"), "foo")
tagGetAttribute(div(foo="bar"), "foo")