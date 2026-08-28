# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 8

from dataclasses import dataclass
from typing import Optional, Any
import re

# Sentinel for R's NA value
class NAValue:
    def __repr__(self):
        return "NA"
    def __str__(self):
        return "NA"

NA = NAValue()

@dataclass
class Response:
    status_code: int
    url: str
    method: str
    headers: dict
    body: bytes
    timing: Optional[dict] = None

# r2py:entity:resp
def response(status_code: int = 200, url: str = "https://example.com", method: str = "GET", body: bytes = b"", timing: Optional[dict] = None, headers=None) -> Response:
    if headers is None:
        headers = {}
    
    if isinstance(headers, str):
        headers = _parse_header_string(headers)
    elif isinstance(headers, dict):
        headers = dict(headers)
    else:
        headers = dict(headers)
    
    header_names_lower = [name.lower() for name in headers.keys()]
    if "date" not in header_names_lower:
        headers["Date"] = "Wed, 01 Jan 2020 00:00:00 UTC"
    
    return Response(
        status_code=int(status_code),
        url=url,
        method=method,
        headers=headers,
        body=body,
        timing=timing
    )

def _parse_header_string(header_str: str) -> dict:
    parts = header_str.split(":")
    if len(parts) == 2:
        return {parts[0].strip(): parts[1].strip()}
    return {}

def _parse_media(content_type_str: str) -> dict:
    parts = content_type_str.split(";")
    media_type = parts[0].strip()
    charset = None
    
    for part in parts[1:]:
        part = part.strip()
        if part.lower().startswith("charset="):
            charset = part.split("=", 1)[1].strip().strip('"\'')
    
    return {
        "type": media_type,
        "charset": charset
    }

def _resp_header_exists(resp: Response, header: str) -> bool:
    header_lower = header.lower()
    return any(name.lower() == header_lower for name in resp.headers.keys())

def _resp_header(resp: Response, header: str) -> Optional[str]:
    header_lower = header.lower()
    for name, value in resp.headers.items():
        if name.lower() == header_lower:
            return value
    return None

# r2py:entity:resp_content_type
def resp_content_type(resp: Response) -> Any:
    if _resp_header_exists(resp, "content-type"):
        content_type_header = _resp_header(resp, "content-type")
        parsed = _parse_media(content_type_header)
        return parsed.get("type")
    else:
        return NA

# r2py:entity:resp_encoding
def resp_encoding(resp: Response) -> str:
    if _resp_header_exists(resp, "content-type"):
        content_type_header = _resp_header(resp, "content-type")
        parsed = _parse_media(content_type_header)
        return parsed.get("charset") or "UTF-8"
    else:
        return "UTF-8"

def r_print(value: Any) -> None:
    """Print value in R format."""
    if isinstance(value, NAValue):
        print("[1] NA")
    elif isinstance(value, str):
        print(f'[1] "{value}"')
    elif isinstance(value, (int, float)):
        print(f"[1] {value}")
    else:
        print(f"[1] {value}")

# r2py:entity:resp
resp = response(headers="Content-type: text/html; charset=utf-8")
# r2py:entity:resp_content_type
r_print(resp_content_type(resp))
# r2py:entity:resp_encoding
r_print(resp_encoding(resp))

# r2py:entity:resp_1
resp = response()
# r2py:entity:resp_content_type_1
r_print(resp_content_type(resp))
# r2py:entity:resp_encoding_1
r_print(resp_encoding(resp))