# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import shiny
from shiny import render

# Note: httpResponse is a low-level server function in R Shiny. 
# In Python's shiny library, response handling is typically managed by the 
# underlying ASGI server (Starlette). To simulate this specific behavior:

from starlette.responses import Response

# Equivalent to the provided R code logic
# r2py:entity:httpResponse
response = Response(
    content="The requested method was not allowed",
    status_code=405,
    media_type="text/plain"
)