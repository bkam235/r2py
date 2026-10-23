# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_content_type.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr2\help
# lines: 9

from email.message import Message


def make_response(headers=None):
    """Create a minimal mock response with the given raw header string."""
    return {"headers": headers or ""}


def resp_content_type(resp):
    """Return the MIME type from the Content-Type header, or None if absent."""
    raw = resp["headers"]
    if not raw:
        return None
    m = Message()
    m["content-type"] = raw.split(":", 1)[1].strip() if ":" in raw else raw
    ct = m.get_content_type()
    return ct if ct != "text/plain" or "content-type" in raw.lower() else None


def resp_encoding(resp):
    """Return the charset from the Content-Type header, or None if absent."""
    raw = resp["headers"]
    if not raw:
        return None
    m = Message()
    m["content-type"] = raw.split(":", 1)[1].strip() if ":" in raw else raw
    return m.get_param("charset")


# Response with Content-Type header
resp = make_response(headers="Content-type: text/html; charset=utf-8")
print(resp_content_type(resp))   # text/html
print(resp_encoding(resp))       # utf-8

# No Content-Type header
resp = make_response()
print(resp_content_type(resp))   # None
print(resp_encoding(resp))       # None
