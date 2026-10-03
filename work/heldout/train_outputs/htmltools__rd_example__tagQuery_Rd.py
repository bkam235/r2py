# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/htmltools__rd_example__tagQuery_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__tagQuery_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['tagQ']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import pandas as pd

# r2py:entity:tagQ
class Tag:
    def __init__(self, name, children=None, attribs=None, noWS=None, renderHook=None):
        self.name = name
        self.children = children if children is not None else []
        self.attribs = attribs if attribs is not None else {}
        self.noWS = noWS
        self.renderHook = renderHook
        self.parent = None

    def __repr__(self):
        return f"<{self.name} attribs={self.attribs} children={self.children}>"

def div(*args, **kwargs):
    noWS = kwargs.pop('.noWS', None)
    renderHook = kwargs.pop('.renderHook', None)
    return Tag("div", children=list(args), attribs=kwargs, noWS=noWS, renderHook=renderHook)

def a(*args, **kwargs):
    noWS = kwargs.pop('.noWS', None)
    renderHook = kwargs.pop('.renderHook', None)
    return Tag("a", children=list(args), attribs=kwargs, noWS=noWS, renderHook=renderHook)

class TagQuery:
    def __init__(self, tags):
        if isinstance(tags, TagQuery):
            self.root = tags.root
            self.selected = tags.selected
        else:
            # Wrap in pseudo root similar to R's wrapWithPseudoRootTag
            self.root = Tag("pseudoRoot", children=[tags])
            self.root.children[0].parent = self.root
            self._update_parents(self.root)
            self.selected = [tags] if isinstance(tags, Tag) else []
            if not self.selected and isinstance(tags, list):
                # Basic implementation of finding tags in list
                self.selected = [t for t in tags if isinstance(t, Tag)]

    def _update_parents(self, node):
        for child in node.children:
            if isinstance(child, Tag):
                child.parent = node
                self._update_parents(child)
            elif isinstance(child, list):
                for subchild in child:
                    if isinstance(subchild, Tag):
                        subchild.parent = node
                        self._update_parents(subchild)

    def find(self, tag_name):
        results = []
        def traverse(node):
            if isinstance(node, Tag) and node.name == tag_name:
                results.append(node)
            if hasattr(node, 'children'):
                for child in node.children:
                    if isinstance(child, Tag):
                        traverse(child)
        
        traverse(self.root)
        # Return a wrapper to allow chaining (like R's tagQuery)
        # In the R script, find() returns a tagQuery object with new selection
        new_query = TagQuery(self.root)
        new_query.selected = results
        return new_query

    def addClass(self, class_name):
        for tag in self.selected:
            if isinstance(tag, Tag):
                current_class = tag.attribs.get('class', '')
                if current_class:
                    tag.attribs['class'] = f"{current_class} {class_name}"
                else:
                    tag.attribs['class'] = class_name
        return self

    def __repr__(self):
        return f"TagQuery(selected={self.selected})"

def tagQuery(tags):
    return TagQuery(tags)

# r2py:entity:tagQ_1
print(tagQ)