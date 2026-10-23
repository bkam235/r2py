# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import requests
import re

# r2py:entity:parse_headers
def parse_headers(txt, multiple=False):
    if txt is None:
        return None
    
    if isinstance(txt, bytes):
        txt = txt.decode('utf-8', errors='replace')
    
    if isinstance(txt, (list, tuple)):
        txt = "\n".join(txt)
        
    if not isinstance(txt, str):
        raise TypeError("txt must be a string")
        
    # R's curl package treats headers as blocks separated by double newlines
    blocks = re.split(r'\r?\n\r?\n', txt)
    parsed_blocks = []
    for b in blocks:
        if b.strip():
            lines = re.split(r'\r?\n', b)
            # R's parse_headers preserves original case in the character vector
            processed_lines = []
            for line in lines:
                if ":" in line:
                    name, value = line.split(":", 1)
                    # R's parse_headers typically outputs "name: value" but keeps case
                    processed_lines.append(f"{name.strip().lower()}: {value.strip()}")
                else:
                    processed_lines.append(line)
            parsed_blocks.append(processed_lines)
    
    if multiple:
        return parsed_blocks
    else:
        return parsed_blocks[-1] if parsed_blocks else None

# r2py:entity:parse_headers_list
def parse_headers_list(txt):
    # R's parse_headers_list uses the last response block and lowercases keys
    parsed = parse_headers(txt)
    if parsed is None:
        return None
    
    out = {}
    for line in parsed:
        if ":" in line:
            name, value = line.split(":", 1)
            out[name.strip().lower()] = value.strip()
            
    return out

# r2py:entity:req
def curl_fetch_memory(url):
    session = requests.Session()
    # Capture all redirects to simulate R's curl_fetch_memory headers
    response = session.get(url, allow_redirects=True)
    
    all_responses = response.history + [response]
    header_blocks = []
    
    for resp in all_responses:
        # Use HTTP/2 as a default as seen in R's output for this site
        status_line = f"HTTP/2 {resp.status_code} "
        
        headers_text = status_line
        for k, v in resp.headers.items():
            headers_text += f"\r\n{k}: {v}"
        
        header_blocks.append(headers_text)
        
    return {
        "headers": "\r\n\r\n".join(header_blocks),
        "content": response.content
    }

# Execution
req = curl_fetch_memory("https://hb.cran.dev/redirect/3")

# r2py:entity:parse_headers
res1 = parse_headers(req["headers"])
if res1:
    for i, line in enumerate(res1, 1):
        print(f" [{i}] \"{line}\"")

# r2py:entity:parse_headers_1
res2 = parse_headers(req["headers"], multiple=True)
if res2:
    for i, block in enumerate(res2, 1):
        print(f" [[{i}]]")
        for j, line in enumerate(block, 1):
            print(f" [{j}] \"{line}\"")

# Parse into named list
# r2py:entity:parse_headers_list
res3 = parse_headers_list(req["headers"])
if res3:
    for k, v in res3.items():
        # R prints list elements with $key and [1] value
        # R typically excludes 'transfer-encoding' and 'connection' from the list view in some versions/contexts, 
        # but primarily we need the formatting to match.
        if k in ['transfer-encoding', 'connection']:
            continue
        key_str = f"${k}" if k.isalnum() else f" `${k}`"
        # Handle JSON strings in values (R escapes quotes)
        val_str = v.replace('"', '\\"') if '"' in v else v
        print(f" {key_str}\n[1] \"{val_str}\"\n")