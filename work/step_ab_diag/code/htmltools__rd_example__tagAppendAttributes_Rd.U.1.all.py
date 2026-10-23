import numpy as np

class Tag:
    def __init__(self, tag_name, children=None, **attrs):
        self.tag_name = tag_name
        self.children = children if children is not None else []
        self.attrs = attrs

    def __repr__(self):
        attrs_str = "".join([f' {k}="{v}"' for k, v in self.attrs.items() if v is not None])
        children_str = "".join([str(c) for c in self.children])
        return f"<{self.tag_name}{attrs_str}>{children_str}</{self.tag_name}>"

def div(*args, **kwargs):
    return Tag("div", children=list(args), **kwargs)

def a(*args, **kwargs):
    return Tag("a", children=list(args), **kwargs)

def tagAppendAttributes(tag, **attrs):
    # Handle .cssSelector logic
    if ".cssSelector" in attrs:
        selector = attrs.pop(".cssSelector")
        for child in tag.children:
            if isinstance(child, Tag) and child.tag_name == selector:
                for k, v in attrs.items():
                    if v is None:
                        child.attrs.pop(k, None)
                    else:
                        child.attrs[k] = v
        return tag
    
    # Standard append to root tag
    for k, v in attrs.items():
        if v is None: # R's NA in tagAppendAttributes removes the attribute
            tag.attrs.pop(k, None)
        else:
            tag.attrs[k] = v
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attrs

def tagGetAttribute(tag, attr):
    return tag.attrs.get(attr)

# Main Execution
html = div(a())
tagAppendAttributes(html, **{"class": "foo"})
tagAppendAttributes(html, **{".cssSelector": "a", "class": "bar"})
tagAppendAttributes(html, **{"contenteditable": None}) # NA maps to None for removal

# These calls produce values that R prints
res_has = tagHasAttribute(div(foo="bar"), "foo")
res_get = tagGetAttribute(div(foo="bar"), "foo")

# To match R's output for the final variables
tagHasAttribute = res_has
tagGetAttribute = res_get