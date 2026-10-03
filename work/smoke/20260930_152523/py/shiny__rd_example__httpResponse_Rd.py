# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

# Since the environment seems to lack 'shiny', and the R code primarily uses 
# httpResponse (which is a data constructor), we implement the logic manually.

# In Python, suppressPackageStartupMessages is not needed for imports.
pass

# r2py:entity:httpResponse
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
    # R assigns class "httpResponse". In Python, we can't easily change class of a dict, 
    # but we can return it as is or wrap it.
    return resp

# r2py:entity:httpResponse
print(httpResponse(status=405,
             content_type="text/plain",
             content="The requested method was not allowed"
))