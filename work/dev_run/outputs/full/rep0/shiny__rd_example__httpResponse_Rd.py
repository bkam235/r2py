# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import shiny

# R: suppressPackageStartupMessages(library(shiny))
# Python: library import is handled by 'import shiny'

# handled by 'import shiny'

# r2py:entity:httpResponse
def httpResponse(status=200, content_type="text/html; charset=UTF-8", content="", headers=None):
    if headers is None:
        headers = {}
    else:
        headers = dict(headers)
        
    if "X-UA-Compatible" not in headers:
        headers["X-UA-Compatible"] = "IE=edge,chrome=1"
        
    resp = {
        "status": status,
        "content_type": content_type,
        "content": content,
        "headers": headers
    }
    # In R, class(resp) <- "httpResponse" is set. 
    # In Python, we represent this as a dictionary reflecting the R structure.
    return resp

# Execute the function call from the R script
# r2py:entity:httpResponse
result = httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
)