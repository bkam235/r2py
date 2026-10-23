# r2py crawler metadata
# package: httr2
# source_type: rd_example
# topic: resp_content_type.Rd
# Translated from R to Python

import requests
from email.message import Message
import re

class Response:
    """Simple response object to mimic httr2 behavior"""
    def __init__(self, headers=None):
        self.headers = headers or {}

    def get_content_type(self):
        """Extract content type from headers"""
        content_type = self.headers.get('Content-type', None)
        if content_type:
            return content_type.split(';')[0]
        return None

    def get_encoding(self):
        """Extract encoding from headers"""
        content_type = self.headers.get('Content-type', '')
        match = re.search(r'charset=([^;]+)', content_type)
        if match:
            return match.group(1).strip()
        return None

# Create response with Content-Type header
resp1 = Response(headers={'Content-type': 'text/html; charset=utf-8'})
print(f"Content-Type: {resp1.get_content_type()}")
print(f"Encoding: {resp1.get_encoding()}")

# Create response without Content-Type header
print("\n--- Response without Content-Type header ---")
resp2 = Response()
print(f"Content-Type: {resp2.get_content_type()}")
print(f"Encoding: {resp2.get_encoding()}")
