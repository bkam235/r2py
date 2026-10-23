import numpy as np

class Tag:
    def __init__(self, tag_name, children=None, **attrs):
        self.tag_name = tag_name
        self.children = children if children is not None else []
        self.attributes = attrs

    def __repr__(self):
        attrs_str = "".join([f' {k}="{v}"' for k, v in self.attributes.items() if v is not None])
        inner = "".join([str(c) for c in self.children])
        return f"<{self.tag_name}{attrs_str}>{inner}</{self.tag_name}>"

def div(*children, **attrs):
    return Tag("div", children=list(children), **attrs)

def a(*children, **attrs):
    return Tag("a", children=list(children), **attrs)

def tagAppendAttributes(tag, **attrs):
    # Handle the special .cssSelector argument
    css_selector = attrs.pop(".cssSelector", None)
    
    if css_selector:
        # Simple implementation: find children with tag name matching selector
        # In the example, .cssSelector = "a" targets the <a> tag
        for child in tag.children:
            if isinstance(child, Tag) and child.tag_name == css_selector:
                for k, v in attrs.items():
                    if v is None: # Handle NA
                        child.attributes.pop(k, None)
                    else:
                        child.attributes[k] = v
    else:
        for k, v in attrs.items():
            if v is None: # Handle NA (R: contenteditable = NA)
                tag.attributes.pop(k, None)
            else:
                tag.attributes[k] = v
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attributes

def tagGetAttribute(tag, attr):
    return tag.attributes.get(attr)

# R: html <- div(a())
html = div(a())

# R: tagAppendAttributes(html, class = "foo")
tagAppendAttributes(html, class_="foo") # 'class' is reserved in Python

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
tagAppendAttributes(html, .cssSelector="a", class_="bar")

# R: tagAppendAttributes(html, contenteditable = NA)
# In Python, we represent NA as None for this context
tagAppendAttributes(html, contenteditable=None)

# R: tagHasAttribute(div(foo = "bar"), "foo")
# We must use a variable or the function call result directly
div_test = div(foo="bar")
tagHasAttribute_res = tagHasAttribute(div_test, "foo")

# R: tagGetAttribute(div(foo = "bar"), "foo")
div_test_2 = div(foo="bar")
tagGetAttribute_res = tagGetAttribute(div_test_2, "foo")

# Note: The R code uses 'class' which is a keyword in Python, 
# but for the internal attribute keys, we keep them as strings.
# In the Tag class, the keys are strings, so 'class' is fine as a key.
# I've used class_ in the function call to avoid syntax errors.
# Correcting the attribute keys back to "class" inside the logic.
def tagAppendAttributes_fixed(tag, **attrs):
    # Map class_ back to class
    normalized_attrs = {("class" if k == "class_" else k): v for k, v in attrs.items()}
    css_selector = normalized_attrs.pop(".cssSelector", None)
    
    if css_selector:
        for child in tag.children:
            if isinstance(child, Tag) and child.tag_name == css_selector:
                for k, v in normalized_attrs.items():
                    if v is None:
                        child.attributes.pop(k, None)
                    else:
                        child.attributes[k] = v
    else:
        for k, v in normalized_attrs.items():
            if v is None:
                tag.attributes.pop(k, None)
            else:
                tag.attributes[k] = v
    return tag

# Redoing the calls with the fixed function to ensure "class" is the key
html = div(a())
tagAppendAttributes_fixed(html, class_="foo")
tagAppendAttributes_fixed(html, .cssSelector="a", class_="bar")
tagAppendAttributes_fixed(html, contenteditable=None)