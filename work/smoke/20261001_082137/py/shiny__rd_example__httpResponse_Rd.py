# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# r2py:entity:httpResponse
def httpResponse(status=200, content_type="text/html; charset=UTF-8", content="", headers=None):
    if headers is None:
        headers = {}
    else:
        headers = dict(headers)
    
    if "X-UA-Compatible" not in headers:
        headers["X-UA-Compatible"] = "IE=edge,chrome=1"
    
    # In R, class(resp) <- "httpResponse" makes it an object of that class.
    # In Python, we can return a dictionary and simulate the structure.
    resp = {
        "status": status,
        "content_type": content_type,
        "content": content,
        "headers": headers
    }
    return resp

# suppressPackageStartupMessages(library(shiny)) is handled by imports if needed, 
# but here we are implementing the specific function logic.

# r2py:entity:httpResponse
print(httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
))