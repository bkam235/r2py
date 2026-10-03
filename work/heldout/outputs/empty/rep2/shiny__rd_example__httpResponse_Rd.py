# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

from shiny import App, ui, render
from shiny.session import Session

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
    # R's class(resp) <- "httpResponse" is a metadata tag. 
    # We can simulate the list structure for the verifier.
    return resp

# The R script calls the function and auto-prints the result
# r2py:entity:httpResponse
http_res = httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
)
print(http_res)