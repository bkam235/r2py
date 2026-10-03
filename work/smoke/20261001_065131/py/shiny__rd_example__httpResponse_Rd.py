# Translated from <R script> by r2py v0.3.0

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
    # In R, class(resp) <- "httpResponse" marks the object type.
    return resp

# suppressPackageStartupMessages(library(shiny)) is handled by the manual implementation above.

# r2py:entity:httpResponse
print(httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
))