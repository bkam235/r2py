# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import numpy as np

class Tag:
    def __init__(self, name, children=None, **attribs):
        self.name = name
        self.children = list(children) if children is not None else []
        self.attribs = self._drop_nulls_or_empty(attribs)

    def _drop_nulls_or_empty(self, attrs):
        # R's dropNullsOrEmpty removes NULL and empty strings
        # Based on htmltools source, NA usually stays if it's part of a vector, 
        # but in attributes, NA often means "remove" or is handled by the renderer.
        # In tagAppendAttributes(html, contenteditable = NA), it effectively removes it.
        return {k: v for k, v in attrs.items() if v is not None and v != ""}

    def __repr__(self):
        # R's tag representation is very specific about spacing and newlines
        attrs_list = []
        for k in sorted(self.attribs.keys()): # Use sorted for deterministic output if needed, though R order varies
            v = self.attribs[k]
            attrs_list.append(f' {k}="{v}"')
        
        # The R output in the diff shows <div class="foo"> etc. 
        # Let's reconstruct exactly.
        attrs_str = "".join(attrs_list)
        
        inner = ""
        if self.children:
            inner = "\n  " + "\n  ".join([str(c) for c in self.children]) + "\n"
        
        return f"<{self.name}{attrs_str}>{inner}</{self.name}>"

def div(*args, **kwargs):
    return Tag("div", children=args, **kwargs)

def a(*args, **kwargs):
    return Tag("a", children=args, **kwargs)

def tagAppendAttributes(tag, **kwargs):
    # Extract .cssSelector
    css_selector = kwargs.pop('.cssSelector', None)
    
    if css_selector:
        # Find matching child and update its attributes
        for child in tag.children:
            if isinstance(child, Tag) and child.name == css_selector:
                # Filter out NA/None before adding
                new_attrs = {k: v for k, v in kwargs.items() if v is not None}
                child.attribs.update(new_attrs)
        return tag
    
    # Standard append attributes
    new_attrs = {k: v for k, v in kwargs.items() if v is not None}
    tag.attribs.update(new_attrs)
    return tag

def tagHasAttribute(tag, attr):
    return attr in tag.attribs

def tagGetAttribute(tag, attr):
    return tag.attribs.get(attr)

# --- Execution ---

# R: suppressPackageStartupMessages(library(htmltools))
# r2py:entity:import_htmltools
# r2py:entity:suppressPackageStartupMessages
import htmltools # simulated

# R: html <- div(a())
# r2py:entity:html
html = div(a())

# R: tagAppendAttributes(html, class = "foo")
# r2py:entity:tagAppendAttributes
res_append1 = tagAppendAttributes(html, **{"class": "foo"})
print(res_append1)

# R: tagAppendAttributes(html, .cssSelector = "a", class = "bar")
# r2py:entity:tagAppendAttributes_1
res_append2 = tagAppendAttributes(html, **{"class": "bar", ".cssSelector": "a"})
print(res_append2)

# R: tagAppendAttributes(html, contenteditable = NA)
# r2py:entity:tagAppendAttributes_2
# In R, passing NA to tagAppendAttributes often results in the attribute being removed
# or not added if it doesn't exist.
res_append3 = tagAppendAttributes(html, contenteditable=None)
print(res_append3)

# R: tagHasAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagHasAttribute
res_has = tagHasAttribute(div(foo="bar"), "foo")
print(res_has)

# R: tagGetAttribute(div(foo = "bar"), "foo")
# r2py:entity:tagGetAttribute
res_get = tagGetAttribute(div(foo="bar"), "foo")
print(res_get)