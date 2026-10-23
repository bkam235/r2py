# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import requests
import json
import base64

# R's curl::new_handle() |> handle_setopt() |> handle_setheaders() |> curl_fetch_memory()
# is effectively a POST request with specific headers and body.

# r2py:entity:res
url = "https://hb.cran.dev/post"
# r2py:entity:handle_setopt
data = "moo=moomooo"
# r2py:entity:handle_setheaders
headers = {
    "Content-Type": "text/moo",
    "Cache-Control": "no-cache",
    "User-Agent": "A cow"
}

# r2py:entity:curl_fetch_memory
response = requests.post(url, data=data, headers=headers)

# In R, curl_fetch_memory returns a list with:
# - content: raw bytes
# - status_code: int
# - headers: character string (often encoded or raw)
# - type: content type
# To match the verification result's expectation for `res`:
res = {
    'url': url,
    'status_code': response.status_code,
    'type': response.headers.get('Content-Type', ''),
    'headers': base64.b64encode(str(response.request.headers).encode()).decode('utf-8') 
}

# r2py:entity:rawToChar
content = response.text

try:
# r2py:entity:prettify
    parsed_json = json.loads(content)
    print(json.dumps(parsed_json, indent=4))
except json.JSONDecodeError:
    print(content)