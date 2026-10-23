import numpy as np

class Tag:
    def __init__(self, name, children=None, **attrs):
        self.name = name
        self.children = children if children is not None else []
        self.attrs = attrs

    def __repr__(self):
        attrs_str = "".join([f' {k}="{v}"' for k, v in self.attrs.items() if v is not None])
        children_str = "".join([str(c) for c in self.children])
        return f"<{self.name}{attrs_str}>{children_str}</{self.name}>"

def div(*args, **kwargs):
    children = [arg for arg in args if arg is not None]
    return Tag("div", children=children, **kwargs)

def a(*args, **kwargs):
    children = [arg for arg in args if arg is not None]
    return Tag("a", children=children, **kwargs)

def tagAppendAttributes(tag, **attrs):
    # If .cssSelector is present, target children
    if ".cssSelector" in attrs:
        selector = attrs.pop(".cssSelector")
        # Simple selector match for the tag name
        for child in tag.children:
            if isinstance(child, Tag) and child.name == selector:
                for k, v in attrs.items():
                    if v is None: # Handling NA (removal)
                        child.attrs.pop(k, None)
                    else:
                        child.attrs[k] = v
        return tag
    
    # Otherwise, append attributes to the root tag
    for k, v in attrs.items():
        if v is None: # Handling NA (removal)
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
tagAppendAttributes(html, cls="foo") # 'class' is reserved in Python, using cls internally if needed, but the R result expects 'class'
# Correction: the R function takes 'class', in Python we can use a dict or kwargs. 
# Since I used **attrs, I can't use 'class' as a keyword.
# I will redefine the function to accept a dict or use a workaround for the specific 'class' key.

def tagAppendAttributes_fixed(tag, **attrs):
    # This is a wrapper to handle the 'class' keyword issue by allowing a dict if needed, 
    # but here we just replace 'cls' with 'class' in the actual storage.
    actual_attrs = { (k if k != 'cls' else 'class'): v for k, v in attrs.items() }
    
    if ".cssSelector" in actual_attrs:
        selector = actual_attrs.pop(".cssSelector")
        for child in tag.children:
            if isinstance(child, Tag) and child.name == selector:
                for k, v in actual_attrs.items():
                    if v is None: child.attrs.pop(k, None)
                    else: child.attrs[k] = v
        return tag
    
    for k, v in actual_attrs.items():
        if v is None: tag.attrs.pop(k, None)
        else: tag.attrs[k] = v
    return tag

# Re-running logic with fixed function to handle 'class'
html = div(a())
tagAppendAttributes_fixed(html, cls="foo")
tagAppendAttributes_fixed(html, cls="bar", **{".cssSelector": "a"})
tagAppendAttributes_fixed(html, contenteditable=None)

# R: tagHasAttribute(div(foo = "bar"), "foo")
res_has = tagHasAttribute(div(foo="bar"), "foo")

# R: tagGetAttribute(div(foo = "bar"), "foo")
res_get = tagGetAttribute(div(foo="bar"), "foo")