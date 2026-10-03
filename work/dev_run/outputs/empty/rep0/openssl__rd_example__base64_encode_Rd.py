# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import base64

# r2py:entity:input
input = "foo = bar + 5".encode('utf-8')
# r2py:entity:message
message = base64.b64encode(input).decode('utf-8')
# r2py:entity:output
output = base64.b64decode(message)
# r2py:entity:identical
print(output == input)