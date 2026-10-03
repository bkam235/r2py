# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

def httpResponse(status=200, content_type="text/html; charset=UTF-8", content="", headers=None):
    if headers is None:
        headers = {}
    else:
        headers = dict(headers)
    
    if 'X-UA-Compatible' not in headers:
        headers['X-UA-Compatible'] = "IE=edge,chrome=1"
        
    resp = {
        'status': status,
        'content_type': content_type,
        'content': content,
        'headers': headers
    }
    # In R, class(resp) <- "httpResponse" is set. 
    # In Python, we can simulate this by adding a __class__ attribute or just keeping it as a dict.
    return resp

# suppressPackageStartupMessages(library(shiny)) is essentially a no-op for the logic here
# as we are implementing the core function manually.

# r2py:entity:httpResponse
print(httpResponse(status=405,
                   content_type="text/plain",
                   content="The requested method was not allowed"))