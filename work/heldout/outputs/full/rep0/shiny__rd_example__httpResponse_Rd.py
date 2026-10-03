# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

from shiny import App, ui, render
from shiny.session import Session
import pandas as pd
import numpy as np
from plotnine import *

# r2py:entity:httpResponse
def httpResponse(status=200, content_type="text/html; charset=UTF-8", content="", headers=None):
    """
    Equivalent to R's shiny::httpResponse
    """
    if headers is None:
        headers = {}
    
    # Ensure headers is a dict
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
    # In Python, we return the dict as it's the closest data structure.
    return resp

# R auto-prints the result of the last expression
# r2py:entity:httpResponse
result = httpResponse(
    status=405,
    content_type="text/plain",
    content="The requested method was not allowed"
)
print(result)