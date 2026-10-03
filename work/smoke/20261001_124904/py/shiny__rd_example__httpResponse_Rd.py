# Translated from <R script> by r2py v0.3.0

def httpResponse(status=200, content_type="text/html; charset=UTF-8", content="", headers=None):
    """
    Replicate R's shiny::httpResponse which returns a list with class 'httpResponse'.
    """
    if headers is None:
        headers = {}
    
    # Ensure headers is a dictionary
    headers = dict(headers)
    
    if "X-UA-Compatible" not in headers:
        headers["X-UA-Compatible"] = "IE=edge,chrome=1"
        
    resp = {
        "status": status,
        "content_type": content_type,
        "content": content,
        "headers": headers
    }
    # In Python, we can't simply assign a class to a dict like R's class(resp) <- "httpResponse",
    # but for verification of the data structure, a dict is the equivalent of an R list.
    return resp

# R: suppressPackageStartupMessages(library(shiny))
# No-op in Python translation

# r2py:entity:httpResponse
print(httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
))