# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 7

import lxml.etree as etree

# r2py:entity:x
x = etree.fromstring("<bar>123</bar>")
# r2py:entity:xml_name
print(x.tag)

# r2py:entity:y
y = etree.fromstring("<bar><baz>1</baz>abc<foo /></bar>")
# r2py:entity:z
z = list(y)
# r2py:entity:xml_name_1
print([child.tag for child in y])