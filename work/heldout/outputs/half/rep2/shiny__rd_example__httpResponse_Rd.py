# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import shiny

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
    # To simulate class(resp) <- "httpResponse"
    # In Python, we can't easily change the class of a dict, 
    # but for the purpose of this data structure:
    return resp

# suppressPackageStartupMessages(library(shiny)) is handled by import shiny
# Execute the function call and print result to match R auto-printing
# r2py:entity:httpResponse
httpResponse_result = httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
)
print(httpResponse_result)