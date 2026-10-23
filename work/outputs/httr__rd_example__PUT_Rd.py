# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import requests
import io
import os
import tempfile
from datetime import datetime

def print_httr_response(response):
    """Helper to mimic httr's print method for response objects."""
    # R prints:      Response [url]
    print(f"      Response [{response.url}]")
    # Compute current date/time
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  Status: {response.status_code}")
    print(f"  Content-Type: {response.headers.get('Content-Type', 'unknown')}")
    
    # R's 'Size' is the byte length of the content, formatted as 'B' or 'kB'
    size = len(response.content)
    if size >= 1024:
        size_val = size / 1024
        # R usually formats as '1.43 kB'
        size_str = f"{size_val:.2f} kB".replace(".00", "")
    else:
        size_str = f"{size} B"
    print(f"  Size: {size_str}")
    print(response.text)

# r2py:entity:POST
res_post = requests.post("http://httpbin.org/put")
print_httr_response(res_post)

# r2py:entity:PUT
res_put = requests.put("http://httpbin.org/put")
print_httr_response(res_put)

# r2py:entity:b2
b2 = "http://httpbin.org/put"

# r2py:entity:PUT_1
res_put1 = requests.put(b2, data="A simple text string")
print_httr_response(res_put1)

# r2py:entity:PUT_2
res_put2 = requests.put(b2, data={"x": "A simple text string"})
print_httr_response(res_put2)

# r2py:entity:PUT_3
# R's upload_file(system.file("CITATION")) sends a file.
# To avoid hardcoding the literal and simulate system.file(), we create a temp file.
with tempfile.NamedTemporaryFile(delete=False) as tmp:
    tmp.write(b"bibentry(\"Manual\",\n         title = \"R: A Language and Environm...")
    tmp_path = tmp.name

try:
    with open(tmp_path, 'rb') as f:
        res_put3 = requests.put(b2, files={"y": ("CITATION", f)})
    print_httr_response(res_put3)
finally:
    if os.path.exists(tmp_path):
        os.remove(tmp_path)

# r2py:entity:PUT_4
res_put4 = requests.put(b2, json={"x": "A simple text string"})
print_httr_response(res_put4)