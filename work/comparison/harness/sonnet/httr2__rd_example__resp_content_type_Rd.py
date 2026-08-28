# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 8

import httpx
from email.message import Message


# r2py:entity:resp
def parse_content_type(content_type_str):
    """Parse a Content-Type header string and return type and charset."""
    m = Message()
    m['content-type'] = content_type_str
    mime_type = m.get_content_type()
    charset = m.get_param('charset')
    return mime_type, charset


def make_response(headers=None):
    """Create a mock response object similar to httr2's response()."""
    if headers is None:
        headers = {}
    if isinstance(headers, str):
        # Parse "Key: Value" string
        key, _, value = headers.partition(':')
        headers = {key.strip(): value.strip()}
    # Add default Date header if not present
    has_date = any(k.lower() == 'date' for k in headers)
    if not has_date:
        headers['Date'] = 'Wed, 01 Jan 2020 00:00:00 UTC'
    return headers


# r2py:entity:resp_content_type
def resp_content_type(resp):
    """Return the MIME type from the Content-Type header, or None if absent."""
    header_names_lower = [k.lower() for k in resp]
    if 'content-type' in header_names_lower:
        ct_value = next(v for k, v in resp.items() if k.lower() == 'content-type')
        mime_type, _ = parse_content_type(ct_value)
        return mime_type
    else:
        return None


# r2py:entity:resp_encoding
def resp_encoding(resp):
    """Return the charset from the Content-Type header, defaulting to 'UTF-8'."""
    header_names_lower = [k.lower() for k in resp]
    if 'content-type' in header_names_lower:
        ct_value = next(v for k, v in resp.items() if k.lower() == 'content-type')
        _, charset = parse_content_type(ct_value)
        return charset if charset is not None else 'UTF-8'
    else:
        return 'UTF-8'


# Response with Content-Type header
# r2py:entity:resp
resp = make_response(headers="Content-type: text/html; charset=utf-8")
# r2py:entity:resp_content_type
print(resp_content_type(resp))
# r2py:entity:resp_encoding
print(resp_encoding(resp))

# No Content-Type header
# r2py:entity:resp_1
resp = make_response()
# r2py:entity:resp_content_type_1
print(resp_content_type(resp))
# r2py:entity:resp_encoding_1
print(resp_encoding(resp))