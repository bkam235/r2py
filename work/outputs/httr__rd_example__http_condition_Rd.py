# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import requests

# r2py:entity:f
def f(url):
    try:
        response = requests.get(url)
        # raise_for_status() raises an HTTPError for 4xx or 5xx responses
        response.raise_for_status()
        return response
    except requests.exceptions.HTTPError as e:
        status_code = e.response.status_code
        # R's httr logic: match specific codes first, then general classes (400, 500)
        if status_code == 404:
            return "That url doesn't exist"
        elif status_code == 403:
            return "You need to authenticate!"
        elif status_code == 400:
            return "You made a mistake!"
        elif 400 <= status_code < 500:
            # This mimics the http_400 catch-all if specific 400 wasn't hit
            # but in the R example, http_400 usually refers to the 4xx class
            return "You made a mistake!"
        elif 500 <= status_code < 600:
            return "The server screwed up"
        else:
            return "An HTTP error occurred"
    except Exception as e:
        return str(e)

# r2py:entity:f_1
print(f("http://httpbin.org/status/404"))
# r2py:entity:f_2
print(f("http://httpbin.org/status/403"))
# r2py:entity:f_3
print(f("http://httpbin.org/status/505"))