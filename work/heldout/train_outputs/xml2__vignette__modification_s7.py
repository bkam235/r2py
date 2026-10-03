# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 12

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/xml2__vignette__modification_s7.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xml2__vignette__modification_s7.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

from lxml import etree
import copy

# r2py:entity:xml_children
def xml_children(x):
    return list(x)

# r2py:entity:xml_add_child
def xml_add_child(x, value, copy_node=True):
    if copy_node:
        # If the value is already an element, deepcopy it to simulate R's .copy = TRUE
        if isinstance(value, etree._Element):
            node = copy.deepcopy(value)
        else:
            node = value
    else:
        node = value
    
    x.append(node)
    return node

# x <- read_xml("<parent><child>1</child><child>2<child>3</child></child></parent>")
# r2py:entity:x
x = etree.fromstring("<parent><child>1</child><child>2<child>3</child></child></parent>")

# children <- xml_children(x)
children = xml_children(x)

# t1 <- children[[1]]
# r2py:entity:t1
t1 = children[0]

# t2 <- children[[2]]
# r2py:entity:t2
t2 = children[1]

# t3 <- xml_children(children[[2]])[[1]]
# r2py:entity:t3
t3 = xml_children(children[1])[0]

# xml_add_child(t1, t3)
# In R's xml2, adding a node that already exists in the tree moves it.
# To replicate that, we set copy_node=False for existing nodes.
xml_add_child(t1, t3, copy_node=False)
# r2py:entity:x_1
x_1 = x

# xml_add_child(t1, read_xml("<test/>"))
# r2py:entity:xml_add_child_1
new_node = etree.fromstring("<test/>")
xml_add_child(t1, new_node)
# r2py:entity:x_2
x_2 = x