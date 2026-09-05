# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/diffobj__vignette__diffobj_chunk18.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'diffobj__vignette__diffobj_chunk18.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['v2']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import numpy as np
import difflib

# r2py:entity:v1
v1 = np.arange(1, 50001)

# r2py:entity:sample
# R's sample(v1, 100) picks 100 random elements from v1
sampled_elements = np.random.choice(v1, 100, replace=False)

# v1[-sample(v1, 100)] removes the sampled elements from v1
# Using setdiff1d to remove the sampled elements
v2 = np.setdiff1d(v1, sampled_elements)

# r2py:entity:diffChr
def diff_chr_mimic(a, b, word_diff=False):
    """
    Mimics the visual output of R's diffobj::diffChr.
    R output format:
    < v1             > v2           
    @@ start,len    @@ start,len   
    line_num         line_num
    < line            ~             # deletion
    """
    a_str = [str(x) for x in a]
    b_str = [str(x) for x in b]
    
    matcher = difflib.SequenceMatcher(None, a_str, b_str)
    
    print(f"< v1             > v2")
    
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'equal':
            continue
            
        # Create hunk header mimic
        # R format: @@ line,len @@ line,len
        # We approximate the context around the change
        ctx = 2
        start_a = max(0, i1 - ctx)
        end_a = min(len(a_str), i2 + ctx)
        start_b = max(0, j1 - ctx)
        end_b = min(len(b_str), j2 + ctx)
        
        len_a = end_a - start_a
        len_b = end_b - start_b
        
        print(f"@@ {start_a+1},{len_a} @@ {start_b+1},{len_b} @@")
        
        # Print context and changes
        for idx in range(start_a, end_a):
            val_a = a_str[idx]
            # Determine if this index is part of the change or just context
            if i1 <= idx < i2:
                prefix_a = "< "
            else:
                prefix_a = "  "
            
            # Find corresponding value in b
            # This is a simplification of the side-by-side view
            if i1 <= idx < i2:
                # it's a change/deletion. Find what replaced it in b.
                # In a simple deletion, we just put ~
                # In a replacement, we put the value from b.
                if tag == 'replace':
                    # Map idx in a to something in b
                    offset = idx - i1
                    if j1 <= j1 + offset < j2:
                        val_b = b_str[j1 + offset]
                        prefix_b = "  "
                    else:
                        val_b = "~"
                        prefix_b = "  "
                elif tag == 'delete':
                    val_b = "~"
                    prefix_b = "  "
                else: # insert
                    val_b = "~"
                    prefix_b = "  "
            else:
                # context. Find index in b.
                # SequenceMatcher tags 'equal' separately, but for the context 
                # lines around the op, we need to align.
                # a_str[idx] is equal to b_str[something]
                # This is complex for a mimic, so we simplify:
                # If it's context, it should appear in both.
                # We find where val_a exists in b within the current hunk.
                try:
                    # Simple alignment for context: find match in b_str near j1
                    match_idx = -1
                    for k in range(start_b, end_b):
                        if b_str[k] == val_a:
                            match_idx = k
                            break
                    if match_idx != -1:
                        val_b = b_str[match_idx]
                        prefix_b = "  "
                    else:
                        val_b = "~"
                        prefix_b = "  "
                except:
                    val_b = "~"
                    prefix_b = "  "

            print(f"{idx+1: <10} {val_b if val_b else '~': >10}")
            # Note: This is a very crude approximation of the complex diffobj layout.
            # The actual diffobj output is a multi-column table.
            
# R called diffChr(v1, v2, word.diff=FALSE)
# We replace the manual print loop with the mimic function
# r2py:entity:diffChr
diff_chr_mimic(v1, v2, word_diff=False)