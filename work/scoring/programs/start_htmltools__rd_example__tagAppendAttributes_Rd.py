# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

from shiny import ui
import pandas as pd
import numpy as np
from plotnine import *

# R: html <- div(a())
# r2py:entity:html
html = ui.div(ui.a())

# R: tagAppendAttributes(html, class_val= "foo")
# In shiny for python, we modify the attributes dictionary of the element
# r2py:entity:tagAppendAttributes
html.attributes["class"] = "foo"

# R: tagAppendAttributes(html, .cssSelector = "a", class_val= "bar")
# Python implementation: find the child element matching the selector and update attributes
# r2py:entity:tagAppendAttributes_1
for child in html.children:
    if hasattr(child, "tag_name") and child.tag_name == "a":
        child.attributes["class"] = "bar"

# R: tagAppendAttributes(html, contenteditable = NA)
# Removing an attribute is typically done by deleting the key or setting to None
# r2py:entity:tagAppendAttributes_2
if "contenteditable" in html.attributes:
    del html.attributes["contenteditable"]

# R: tagHasAttribute(div(foo = "bar"), "foo")
# Mimicking tagHasAttribute logic
# r2py:entity:tagHasAttribute
test_div = ui.div(foo="bar")
has_attr = "foo" in test_div.attributes

# R: tagGetAttribute(div(foo = "bar"), "foo")
# Mimicking tagGetAttribute logic
# r2py:entity:tagGetAttribute
get_attr = test_div.attributes.get("foo")