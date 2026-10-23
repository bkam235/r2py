# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import os
import tempfile

# r2py:entity:f
f = tempfile.mktemp()
# r2py:entity:writeLines
with open(f, "w") as file:
    file.write("hello\nworld")

# r2py:entity:gsub_file
with open(f, "r") as file:
    content = file.read()

content = content.replace("world", "woRld")

with open(f, "w") as file:
    file.write(content)

# r2py:entity:file_string
with open(f, "r") as file:
    print(file.read())