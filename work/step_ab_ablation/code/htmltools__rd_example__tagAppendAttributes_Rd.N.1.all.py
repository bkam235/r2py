from shiny import ui
import numpy as np

def tagAppendAttributes(tag, **attrs):
    # Handle .cssSelector for nested elements
    css_selector = attrs.pop(".cssSelector", None)
    
    if css_selector:
        # Simplified selector logic for the example: find child matching tag name
        for child in tag.children:
            if hasattr(child, "tag_name") and child.tag_name == css_selector:
                for k, v in attrs.items():
                    if v is np.nan:
                        child.attributes.pop(k, None)
                    else:
                        child.attributes[k] = v
    else:
        for k, v in attrs.items():
            if v is np.nan:
                tag.attributes.pop(k, None)
            else:
                tag.attributes[k] = v
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attributes

def tagGetAttribute(tag, attr):
    return tag.attributes.get(attr)

# html <- div(a())
html = ui.div(ui.a())

# tagAppendAttributes(html, class = "foo")
tagAppendAttributes = tagAppendAttributes(html, class_="foo")

# tagAppendAttributes(html, .cssSelector = "a", class = "bar")
tagAppendAttributes_1 = tagAppendAttributes(html, .cssSelector="a", class_="bar")

# tagAppendAttributes(html, contenteditable = NA)
tagAppendAttributes_2 = tagAppendAttributes(html, contenteditable=np.nan)

# tagHasAttribute(div(foo = "bar"), "foo")
tagHasAttribute = tagHasAttribute(ui.div(foo="bar"), "foo")

# tagGetAttribute(div(foo = "bar"), "foo")
tagGetAttribute = tagGetAttribute(ui.div(foo="bar"), "foo")