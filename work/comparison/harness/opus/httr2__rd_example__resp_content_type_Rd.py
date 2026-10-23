# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 8

import re


# r2py:entity:resp
def parse_content_type(header_value):
    """Parse a Content-Type header value into type and parameters."""
    parts = [p.strip() for p in header_value.split(";")]
    media_type = parts[0].strip().lower()
    params = {}
    for part in parts[1:]:
        if "=" in part:
            key, value = part.split("=", 1)
            params[key.strip().lower()] = value.strip()
    return {"type": media_type, "params": params}


class Response:
    def __init__(self, status_code=200, url="https://example.com", method="GET",
                 headers=None, body=b"", timing=None):
        self.status_code = status_code
        self.url = url
        self.method = method
        self.body = body
        self.timing = timing
        self.headers = {}
        if headers is not None:
            if isinstance(headers, str):
                # Parse header string(s)
                for line in headers.split("\n"):
                    line = line.strip()
                    if ":" in line:
                        key, value = line.split(":", 1)
                        self.headers[key.strip()] = value.strip()
            elif isinstance(headers, dict):
                self.headers = headers
        # Add default Date header if not present
        if "date" not in {k.lower() for k in self.headers}:
            self.headers["Date"] = "Wed, 01 Jan 2020 00:00:00 UTC"


def response(status_code=200, url="https://example.com", method="GET",
             headers=None, body=b"", timing=None):
    return Response(status_code=status_code, url=url, method=method,
                    headers=headers, body=body, timing=timing)


def resp_header_exists(resp, header):
    return header.lower() in {k.lower() for k in resp.headers}


def resp_header(resp, header):
    for k, v in resp.headers.items():
        if k.lower() == header.lower():
            return v
    return None


# r2py:entity:resp_content_type
def resp_content_type(resp):
    if resp_header_exists(resp, "content-type"):
        ct = resp_header(resp, "content-type")
        parsed = parse_content_type(ct)
        return parsed["type"]
    else:
        return None  # represents NA_character_


# r2py:entity:resp_encoding
def resp_encoding(resp):
    if resp_header_exists(resp, "content-type"):
        ct = resp_header(resp, "content-type")
        parsed = parse_content_type(ct)
        return parsed["params"].get("charset", "UTF-8")
    else:
        return "UTF-8"


# r2py:entity:resp_content_type
def r_format(val):
    """Format a value like R's default print for a length-1 character vector."""
    if val is None:
        return '[1] NA'
    else:
        return f'[1] "{val}"'


# r2py:entity:resp
resp = response(headers="Content-type: text/html; charset=utf-8")
# r2py:entity:resp_content_type
print(r_format(resp_content_type(resp)))
# r2py:entity:resp_encoding
print(r_format(resp_encoding(resp)))

# No Content-Type header
# r2py:entity:resp_1
resp = response()
# r2py:entity:resp_content_type_1
print(r_format(resp_content_type(resp)))
# r2py:entity:resp_encoding_1
print(r_format(resp_encoding(resp)))