from shiny import ui
import numpy as np

# Helper to mimic htmltools' tag system
def tagAppendAttributes(tag, **attrs):
    """
    Mimics R's tagAppendAttributes. 
    If .cssSelector is provided, it targets child elements.
    """
    selector = attrs.pop(".cssSelector", None)
    
    # If a selector is provided, we look for children to modify
    if selector:
        # In shiny.ui, elements are stored in 'children' as a list
        if hasattr(tag, "children") and tag.children:
            for child in tag.children:
                # Simple check for tag name matching the selector
                if hasattr(child, "tag_name") and child.tag_name == selector:
                    for k, v in attrs.items():
                        if v is np.nan:
                            # Simulate removing attribute if NA
                            if hasattr(child, "attrs"):
                                child.attrs.pop(k, None)
                        else:
                            if not hasattr(child, "attrs"):
                                child.attrs = {}
                            child.attrs[k] = v
    else:
        # Modify the tag itself
        if not hasattr(tag, "attrs"):
            tag.attrs = {}
        for k, v in attrs.items():
            if v is np.nan:
                tag.attrs.pop(k, None)
            else:
                tag.attrs[k] = v
    return tag

def tagHasAttribute(tag, attr):
    """Mimics R's tagHasAttribute"""
    if hasattr(tag, "attrs"):
        return attr in tag.attrs
    return False

def tagGetAttribute(tag, attr):
    """Mimics R's tagGetAttribute"""
    if hasattr(tag, "attrs"):
        return tag.attrs.get(attr)
    return None

# R: html <- div(a())
html = ui.div(ui.a())

# R: tagAppendAttributes(html, class = "foo")
tagAppendAttributes(html, **{"class": "foo"})

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
tagAppendAttributes(html, **{".cssSelector": "a", "class": "bar"})

# R: tagAppendAttributes(html, contenteditable = NA)
tagAppendAttributes(html, **{"contenteditable": np.nan})

# R: tagHasAttribute(div(foo = "bar"), "foo")
# We need to ensure the div has the attribute in our shim
div_foo = ui.div()
div_foo.attrs = {"foo": "bar"}
tagHasAttribute(div_foo, "foo")

# R: tagGetAttribute(div(foo = "bar"), "foo")
div_foo_2 = ui.div()
div_foo_2.attrs = {"foo": "bar"}
tagGetAttribute(div_foo_2, "foo")