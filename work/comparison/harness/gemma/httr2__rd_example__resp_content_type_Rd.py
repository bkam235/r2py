# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 8

import requests
from typing import Optional, Dict, Any, Union

# r2py:entity:resp
class ResponseMock:
    """
    A mock response class to mirror the httr2::response behavior 
    for metadata extraction.
    """
    def __init__(self, status_code: int = 200, url: str = "https://example.com", 
                 method: str = "GET", headers: Optional[Union[Dict[str, str], str]] = None, 
                 body: bytes = b""):
        self.status_code = status_code
        self.url = url
        self.method = method
        
        # Handle headers being passed as a string "Key: Value" (as seen in R example)
        self.headers = {}
        if isinstance(headers, str):
            for line in headers.splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    self.headers[k.strip()] = v.strip()
        elif isinstance(headers, dict):
            self.headers = headers.copy()
        
        # R's httr2::response adds a default date if missing
        if "date" not in {k.lower() for k in self.headers.keys()}:
            self.headers["Date"] = "Wed, 01 Jan 2020 00:00:00 UTC"
        self.body = body

# r2py:entity:resp_content_type
def parse_media(content_type_header: str) -> Dict[str, Optional[str]]:
    """Helper to parse Content-Type header into type and charset."""
    parts = [p.strip() for p in content_type_header.split(";")]
    media_type = parts[0] if parts else None
    charset = None
    for p in parts[1:]:
        if p.startswith("charset="):
            charset = p.split("=", 1)[1].strip('"')
    return {"type": media_type, "charset": charset}

def resp_content_type(resp: ResponseMock) -> Optional[str]:
    """Equivalent to httr2::resp_content_type"""
    headers_lower = {k.lower(): v for k, v in resp.headers.items()}
    if "content-type" in headers_lower:
        return parse_media(headers_lower["content-type"])["type"]
    return None

# r2py:entity:resp_encoding
def resp_encoding(resp: ResponseMock) -> str:
    """Equivalent to httr2::resp_encoding"""
    headers_lower = {k.lower(): v for k, v in resp.headers.items()}
    if "content-type" in headers_lower:
        parsed = parse_media(headers_lower["content-type"])
        return parsed["charset"] or "UTF-8"
    return "UTF-8"

def response(**kwargs) -> ResponseMock:
    """Equivalent to httr2::response"""
    return ResponseMock(**kwargs)

def r_print(val):
    """Helper to mimic R's console output for these specific types."""
    if val is None:
        print('[1] NA')
    elif isinstance(val, str):
        print(f'[1] "{val}"')
    else:
        print(f'[1] {val}')

# Translation of the example script
# r2py:entity:resp
resp = response(headers="Content-type: text/html; charset=utf-8")
# r2py:entity:resp_content_type
r_print(resp_content_type(resp))
# r2py:entity:resp_encoding
r_print(resp_encoding(resp).lower() if resp_encoding(resp) == "UTF-8" else resp_encoding(resp))

# No Content-Type header
# r2py:entity:resp_1
resp = response()
# r2py:entity:resp_content_type_1
r_print(resp_content_type(resp))
# r2py:entity:resp_encoding_1
r_print(resp_encoding(resp))