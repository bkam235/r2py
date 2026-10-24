import numpy as np

# r2py:entity:html
class Tag:
    def __init__(self, name, children=None, **attribs):
        self.name = name
        self.children = children if children is not None else []
        self.attribs = attribs

    def __repr__(self):
        # R htmltools output is very specific: <div class="foo"><a class="bar"></a></div>
        # No spaces between attributes and tags
        attrs_list = []
        for k, v in self.attribs.items():
            if v is not None and not (isinstance(v, float) and np.isnan(v)):
                attrs_list.append(f'{k}="{v}"')
        
        attrs_str = (" " + " ".join(attrs_list)) if attrs_list else ""
        children_str = "".join([str(c) for c in self.children])
        return f"<{self.name}{attrs_str}>{children_str}</{self.name}>"

def div(*args, **kwargs):
    children = list(args)
    return Tag("div", children=children, **kwargs)

def a(*args, **kwargs):
    children = list(args)
    return Tag("a", children=children, **kwargs)

# r2py:entity:tagAppendAttributes
def tagAppendAttributes(tag, **kwargs):
    css_selector = kwargs.pop(".cssSelector", None)
    
    if css_selector:
        # Simple selector: find children with matching tag name
        for child in tag.children:
            if isinstance(child, Tag) and child.name == css_selector:
                child.attribs.update(kwargs)
        return tag
    
    for k, v in kwargs.items():
        if v is None or (isinstance(v, float) and np.isnan(v)):
            if k in tag.attribs:
                del tag.attribs[k]
        else:
            tag.attribs[k] = v
    return tag

# r2py:entity:tagHasAttribute
def tagHasAttribute(tag, attr):
    return attr in tag.attribs

# r2py:entity:tagGetAttribute
def tagGetAttribute(tag, attr):
    val = tag.attribs.get(attr)
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return None
    return str(val)

# --- Execution ---

# html <- div(a())
# r2py:entity:html
html = div(a())

# tagAppendAttributes(html, class = "foo")
# r2py:entity:tagAppendAttributes
res_append1 = tagAppendAttributes(html, **{"class": "foo"})
print(res_append1)

# tagAppendAttributes(html, .cssSelector = "a", class = "bar")
# r2py:entity:tagAppendAttributes_1
res_append2 = tagAppendAttributes(html, **{".cssSelector": "a", "class": "bar"})
print(res_append2)

# tagAppendAttributes(html, contenteditable = NA)
# r2py:entity:tagAppendAttributes_2
res_append3 = tagAppendAttributes(html, contenteditable=np.nan)
print(res_append3)

# tagHasAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagHasAttribute
tagHasAttribute_res = tagHasAttribute(div(foo="bar"), "foo")
print(tagHasAttribute_res)

# tagGetAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagGetAttribute
tagGetAttribute_res = tagGetAttribute(div(foo="bar"), "foo")
print(tagGetAttribute_res)