# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import numpy as np

# Mocking htmltools functionality as shiny.ui is for UI layout and not attribute manipulation
class HTMLTag:
    def __init__(self, tag_name, children=None, **attrs):
        self.tag_name = tag_name
        self.children = children if children is not None else []
        self.attributes = attrs

    def __repr__(self):
        return f"<{self.tag_name} {self.attributes}>"

def div(*args, **kwargs):
    # Handle positional args as children
    children = list(args)
    # Separate attributes from children (kwargs)
    return HTMLTag("div", children=children, **kwargs)

def a(*args, **kwargs):
    children = list(args)
    return HTMLTag("a", children=children, **kwargs)

def tagAppendAttributes(tag, **attrs):
    # This function in R modifies the tag in place or returns it
    # If .cssSelector is provided, it finds the matching child
    selector = attrs.pop(".cssSelector", None)
    
    if selector:
        # Simple selector logic for 'a'
        for child in tag.children:
            if isinstance(child, HTMLTag) and child.tag_name == selector:
                child.attributes.update(attrs)
    else:
        # Update attributes of the tag itself
        for k, v in attrs.items():
            if v is None or (isinstance(v, float) and np.isnan(v)):
                if k in tag.attributes:
                    del tag.attributes[k]
            else:
                tag.attributes[k] = v
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attributes

def tagGetAttribute(tag, attr):
    return tag.attributes.get(attr)

# R: html <- div(a())
# r2py:entity:html
html = div(a())

# R: tagAppendAttributes(html, class = "foo")
# r2py:entity:tagAppendAttributes
tagAppendAttributes(html, class_="foo") # Use class_ to avoid python keyword 'class'

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
# r2py:entity:tagAppendAttributes_1
tagAppendAttributes(html, .cssSelector="a", class_="bar")

# R: tagAppendAttributes(html, contenteditable = NA)
# r2py:entity:tagAppendAttributes_2
tagAppendAttributes(html, contenteditable=np.nan)

# R: tagHasAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagHasAttribute
tagHasAttribute_res = tagHasAttribute(div(foo="bar"), "foo")

# R: tagGetAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagGetAttribute
tagGetAttribute_res = tagGetAttribute(div(foo="bar"), "foo")