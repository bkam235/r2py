# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/htmltools__rd_example__htmlPreserve_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'htmltools__rd_example__htmlPreserve_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['output']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re
import random

# r2py:entity:markup
def html_preserve(x, inline="auto"):
    if isinstance(x, list):
        x = "\n".join(map(str, x))
    if not x:
        return x
    
    # getOption("htmltools.preserve.raw", FALSE) is FALSE by default
    return f"<!--html_preserve-->{x}<!--/html_preserve-->"

def htmlPreserve(x):
    return html_preserve(x, inline="auto")

# r2py:entity:extracted
def extractPreserveChunks(strval):
    startmarker = "<!--html_preserve-->"
    endmarker = "<!--/html_preserve-->"
    startmarker_len = len(startmarker)
    endmarker_len = len(endmarker)
    pattern = "<!--/?html_preserve-->"
    
    if not isinstance(strval, str):
        strval = "\n".join(map(str, strval))
    
    # Find all occurrences
    startmatches = []
    curr = 0
    while True:
        idx = strval.find(startmarker, curr)
        if idx == -1: break
        startmatches.append(idx + 1) # 1-based
        curr = idx + 1
        
    endmatches = []
    curr = 0
    while True:
        idx = strval.find(endmarker, curr)
        if idx == -1: break
        endmatches.append(idx + 1) # 1-based
        curr = idx + 1
    
    matches = sorted(startmatches + endmatches)
    
    if not matches or matches[0] == -1:
        return {"value": strval, "chunks": {}}
    
    # Determine lengths corresponding to the sorted matches
    all_matches_map = {}
    for m in startmatches: all_matches_map[m] = startmarker_len
    for m in endmatches: all_matches_map[m] = endmarker_len
    lengths = [all_matches_map[m] for m in matches]
    
    boundary_type = [l == startmarker_len for l in lengths]
    preserve_level = []
    lvl = 0
    for b in boundary_type:
        lvl += 1 if b else -1
        preserve_level.append(lvl)
        
    if any(l < 0 for l in preserve_level) or preserve_level[-1] != 0:
        raise ValueError("Invalid nesting of html_preserve directives")
        
    # Top level logic: preserve_level[i] + preserve_level[i-1] == 1
    is_top_level = []
    for i in range(len(preserve_level)):
        prev = preserve_level[i-1] if i > 0 else 0
        is_top_level.append(1 == (preserve_level[i] + prev))
        
    top_level_matches = [matches[i] for i, val in enumerate(is_top_level) if val]
    preserved = {}
    
    # Process from end to start to keep indices valid
    # seq.int(length(top_level_matches) - 1, 1, by = -2)
    for i in range(len(top_level_matches) - 1, 0, -2):
        # In R, i is 1-based index for the pair (start, end)
        # Loop goes: (N, N-1), (N-2, N-3) ... where N is end of last block
        # Actually R's loop: i=length-1 is start, i+1 is end
        # Let's adjust indices to 0-based:
        idx_start = top_level_matches[i-1] - 1
        idx_end = top_level_matches[i] - 1
        
        start_inner = idx_start + startmarker_len
        end_inner = idx_end
        end_outer = idx_end + endmarker_len
        
        # ID generation: preserve + 8 hex bytes
        # Use a fixed seed if needed for stability, but R uses random
        hex_id = "".join(f"{random.randint(0, 255):02x}" for _ in range(8))
        id_str = f"preserve{hex_id}"
        
        # content is substr(strval, start_inner, end_inner - 1)
        # then gsub(pattern, "", content)
        content = strval[start_inner:end_inner]
        content = re.sub(pattern, "", content)
        preserved[id_str] = content
        
        # Replace the block with the ID
        strval = strval[:idx_start] + id_str + strval[end_outer:]
        
    return {"value": strval, "chunks": preserved}

# r2py:entity:output_1
def restorePreserveChunks(strval, chunks):
    for id_str, content in chunks.items():
        strval = strval.replace(id_str, content)
    return strval

# --- Main Script Execution ---

# r2py:entity:markup
markup = "\n".join([
    "This is *emphasized* text in markdown.",
    htmlPreserve("<script>alert(10*2*3);</script>"),
    "Here is some more *emphasized text*."
])

# r2py:entity:extracted
extracted = extractPreserveChunks(markup)

# r2py:entity:markup_1
markup = extracted["value"]

# r2py:entity:output
output = re.sub(r"\*(.*?)\*", r"<em>\1</em>", markup)

# r2py:entity:output_1
output = restorePreserveChunks(output, extracted["chunks"])

# Final output variable for verification
# r2py:entity:output_2
output_2 = output