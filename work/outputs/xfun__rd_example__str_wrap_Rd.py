# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/outputs/xfun__rd_example__str_wrap_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'xfun__rd_example__str_wrap_Rd.r2py_data.json').read_text(encoding='utf-8'))
# r2py:entity:x
# for _r2py_shim_n in ['letters', 'x']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re

# r2py:entity:strwrap
def strwrap(x, width=72, indent=0, exdent=0, prefix="", simplify=True, initial=None):
    if initial is None:
        initial = prefix
    
    if not isinstance(x, (list, tuple)):
        x = [str(x)]
    else:
        x = [str(i) for i in x]
    
    indent_string = " " * indent
    exdent_string = " " * exdent
    
    y = []
    for item in x:
        # R's strwrap splits by whitespace and collapses multiple spaces
        # unless they are within words.
        words = item.split()
        if not words:
            yi = [""]
        else:
            yi = []
            current_line_words = []
            # First line uses 'initial' and 'indent'
            current_prefix = initial + indent_string
            current_max_width = width - len(current_prefix)
            
            line_len = 0
            for word in words:
                w_len = len(word)
                # space + word
                needed = (1 if line_len > 0 else 0) + w_len
                
                if line_len == 0 and needed > current_max_width:
                    # Word is too long for line, but it's the first word
                    current_line_words.append(word)
                    line_len += w_len
                elif needed <= current_max_width:
                    current_line_words.append(word)
                    line_len += needed
                else:
                    # Line is full, wrap to next
                    yi.append(current_prefix + " ".join(current_line_words))
                    # Next lines use 'prefix' and 'exdent'
                    current_prefix = prefix + exdent_string
                    current_max_width = width - len(current_prefix)
                    current_line_words = [word]
                    line_len = len(word)
            
            if current_line_words:
                yi.append(current_prefix + " ".join(current_line_words))
        
        if simplify:
            y.extend(yi)
        else:
            y.append(yi)
            
    return y if simplify else y

# r2py:entity:str_wrap
def one_string(lines):
    return "\n".join(lines)

def str_wrap(*args, **kwargs):
    # xfun::str_wrap calls strwrap(..., simplify = FALSE) and joins
    res = strwrap(*args, **kwargs, simplify=False)
    return [one_string(item) for item in res]

# Execution
# x is provided by shim
# result_strwrap = strwrap(x, width=30)
# result_str_wrap = str_wrap(x, width=30)

# R equivalent calls:
# strwrap(x, width = 30)
# r2py:entity:strwrap
res_strwrap = strwrap(x, width=30)
print(res_strwrap)

# xfun::str_wrap(x, width = 30)
# r2py:entity:str_wrap
res_str_wrap = str_wrap(x, width=30)
print(res_str_wrap)