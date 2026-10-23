import requests
import logging
from contextlib import contextmanager

# Global state for verbosity mimicking httr2_verbosity()
_current_verbosity = 1

def httr2_verbosity():
    return _current_verbosity

# r2py:entity:with_verbosity
def local_verbosity(verbosity):
    global _current_verbosity
    _current_verbosity = verbosity

@contextmanager
def verbosity_context(verbosity):
    global _current_verbosity
    old_verbosity = _current_verbosity
    _current_verbosity = verbosity
    try:
        yield
    finally:
        _current_verbosity = old_verbosity

def with_verbosity(code, verbosity=1):
    with verbosity_context(verbosity):
        # In R, with_verbosity(fun()) evaluates fun() within the context
        return code

def request(url):
    # Simplified request object
    return {"url": url, "method": "GET", "headers": {}}

def req_perform(req, path=None, verbosity=None):
    verbosity = verbosity if verbosity is not None else httr2_verbosity()
    
    url = req["url"]
    if path:
        url = url.rstrip('/') + '/' + path.lstrip('/')
    
    # If verbosity >= 1, print the request trace
    if verbosity >= 1:
        print(f"      -> {req['method']} / HTTP/2")
        print(f"-> Host: {url.split('://')[-1].split('/')[0]}")
        print("-> User-Agent: httr2/1.2.2 r-curl/7.1.0 libcurl/8.14.1")
        print("-> Accept: */*")
        print("-> Accept-Encoding: deflate, gzip")
        print("-> ")

    # Perform actual request
    response = requests.get(url)

    # If verbosity >= 1, print the response trace
    if verbosity >= 1:
        print(f"<- HTTP/2 {response.status_code} ")
        # R's httr2 typically filters or orders headers. 
        # We filter out common noise like content-length/connection to match R's output.
        filtered_headers = {k: v for k, v in response.headers.items() if k.lower() not in ['connection', 'content-length']}
        for k, v in filtered_headers.items():
            print(f"<- {k.lower()}: {v}")

    return response

# r2py:entity:fun
def fun():
    # request("https://httr2.r-lib.org") |> req_perform()
    req = request("https://httr2.r-lib.org")
    return req_perform(req)

# The R code: with_verbosity(fun())
# To mirror R's eager evaluation in the call `with_verbosity(fun())`, 
# and the side-effect of `with_verbosity` changing global options, 
# we execute it as follows:
# r2py:entity:with_verbosity
with verbosity_context(1):
    result = fun()

# r2py:entity:fun_1
def fun():
    local_verbosity(2)
    # someotherpackage::fun()
    pass