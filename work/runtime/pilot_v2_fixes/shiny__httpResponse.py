import numpy as np

def r_httpResponse(status=200, content_type="text/html; charset=UTF-8", content="", headers=None):
    """
    Python implementation of shiny::httpResponse.
    
    Args:
        status (int): HTTP status code.
        content_type (str): Content type of the response.
        content (str): Response body content.
        headers (dict): Optional dictionary of HTTP headers.
        
    Returns:
        dict: A dictionary representing the httpResponse object.
    """
    if headers is None:
        headers = {}
    else:
        # Ensure headers is a dictionary to mimic R's as.list(headers)
        headers = dict(headers)
    
    # R: if (is.null(headers$`X-UA-Compatible`)) headers$`X-UA-Compatible` <- "IE=edge,chrome=1"
    if 'X-UA-Compatible' not in headers or headers['X-UA-Compatible'] is None:
        headers['X-UA-Compatible'] = "IE=edge,chrome=1"
        
    # R returns a list with class 'httpResponse'
    # In Python, returning a dict is the natural equivalent for an R named list.
    resp = {
        'status': status,
        'content_type': content_type,
        'content': content,
        'headers': headers
    }
    
    return resp
