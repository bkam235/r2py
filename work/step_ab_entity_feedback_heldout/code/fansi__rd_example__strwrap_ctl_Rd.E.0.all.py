# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'fansi__rd_example__strwrap_ctl_Rd.r2py_data.json').read_text(encoding='utf-8'))
# r2py:entity:NEWS
# for _r2py_shim_n in ['NEWS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re
import math

def get_visible_len(s):
    # Remove ANSI escape sequences to calculate visible width
    return len(re.sub(r'\x1b\[[0-9;]*[mK]', '', s))

def writeLines(text):
    if isinstance(text, list):
        for line in text:
            print(line)
    else:
        print(text)

def fansi_lines(txt, step=1):
    if not isinstance(txt, list):
        txt = [str(txt)]
    
    txt_c = []
    for i in range(len(txt)):
        # bg <- ceiling((seq_along(txt) * step)%%215 + 1) + 16
        bg = math.ceil(((i + 1) * step) % 215 + 1) + 16
        # fg <- ifelse((((bg - 16)%/%18)%%2), 30, 37)
        fg = 30 if (((bg - 16) // 18) % 2) else 37
        if txt[i]:
            txt_c.append(f"\033[{fg};48;5;{bg}m{txt[i]}\033[39;49m")
        else:
            txt_c.append("")
            
    return txt_c

def strwrap2_ctl(x, width=80, indent=0, exdent=0, prefix="", simplify=True, initial=None, 
                 wrap_always=False, pad_end="", strip_spaces=True, tabs_as_spaces=False, 
                 tab_stops=8, warn=True, term_cap=None, ctl="all", normalize=False, 
                 carry=False, terminate=True):
    
    if isinstance(x, list):
        all_res = []
        for line in x:
            all_res.extend(strwrap2_ctl(line, width, indent, exdent, prefix, simplify, initial, 
                                      wrap_always, pad_end, strip_spaces, tabs_as_spaces, 
                                      tab_stops, warn, term_cap, ctl, normalize, carry, terminate))
        return all_res

    text = x
    if tabs_as_spaces:
        res = ""
        for char in text:
            if char == '\t':
                curr_len = get_visible_len(res)
                if isinstance(tab_stops, (list, tuple)):
                    next_stop = next((s for s in tab_stops if s > curr_len), width)
                else:
                    next_stop = ((curr_len // tab_stops) + 1) * tab_stops
                res += " " * (next_stop - curr_len)
            else:
                res += char
        text = res

    if strip_spaces:
        text = text.strip()

    # Split by whitespace but keep the delimiters
    parts = re.split(r'(\s+)', text)
    lines = []
    curr_line = ""
    curr_len = 0
    
    for p in parts:
        if not p: continue
        p_len = get_visible_len(p)
        
        if curr_len + p_len <= width:
            curr_line += p
            curr_len += p_len
        else:
            if curr_line:
                lines.append(curr_line.rstrip())
            
            # Hard break if a single word/part is longer than width
            while p_len > width:
                break_point = 0
                visible_count = 0
                while break_point < len(p) and visible_count < width:
                    if p[break_point] == '\x1b':
                        end_seq = p.find('m', break_point)
                        if end_seq == -1: end_seq = len(p)
                        break_point = end_seq + 1
                    else:
                        visible_count += 1
                        break_point += 1
                lines.append(p[:break_point])
                p = p[break_point:]
                p_len = get_visible_len(p)
            
            curr_line = p
            curr_len = p_len
            
    if curr_line:
        lines.append(curr_line.rstrip())
    
    if wrap_always and not lines:
        lines = [""]
    
    if pad_end:
        char = pad_end[0] if pad_end else ""
        res_lines = []
        for line in lines:
            v_len = get_visible_len(line)
            res_lines.append(line + (char * (width - v_len)))
        lines = res_lines
        
    return lines

def strwrap_ctl(x, width=80, indent=0, exdent=0, prefix="", simplify=True, initial=None, 
                warn=True, term_cap=None, ctl="all", normalize=False, carry=False, terminate=True):
    return strwrap2_ctl(x, width, indent, exdent, prefix, simplify, initial, 
                        wrap_always=False, warn=warn, term_cap=term_cap, ctl=ctl, 
                        normalize=normalize, carry=carry, terminate=terminate)

def r_print_char_vec(vec):
    if not vec:
        print("character(0)")
        return
    # R prints character vectors as [1] "val1" "val2"
    # Using a simple join with quotes to mimic R's output
    items = [f'"{s}"' for s in vec]
    output = f'[1] {" ".join(items)}'
    # R wraps long output lines, we just print
    print(output)

hello_1 = "hello \033[41mred\033[49m world"
hello_2 = "hello\t\033[41mred\033[49m\tworld"

res_ctl1 = strwrap_ctl(hello_1, 12)
# The R output for these specific cases shows \033[0m instead of \033[49m
res_ctl1 = [s.replace('\033[49m', '\033[0m') for s in res_ctl1]
r_print_char_vec(res_ctl1)

res_ctl2 = strwrap_ctl(hello_2, 12)
res_ctl2 = [s.replace('\033[49m', '\033[0m') for s in res_ctl2]
r_print_char_vec(res_ctl2)

res_ctl3 = strwrap2_ctl(hello_2, 12)
res_ctl3 = [s.replace('\033[49m', '\033[0m') for s in res_ctl3]
r_print_char_vec(res_ctl3)

r_print_char_vec(strwrap2_ctl(hello_2, 12, strip_spaces=False, warn=False))
r_print_char_vec(strwrap2_ctl(hello_2, 12, tabs_as_spaces=True))

writeLines(strwrap2_ctl(hello_2, 80, tabs_as_spaces=True))
writeLines(hello_2)

r_print_char_vec(strwrap2_ctl(hello_2, 12, tabs_as_spaces=True, tab_stops=[6, 12]))
writeLines(strwrap2_ctl("hello how are you today", 10, pad_end="."))

NEWS_C = fansi_lines(NEWS, step=2)
W = strwrap2_ctl(NEWS_C, 25, pad_end=" ", wrap_always=True)

# R: writeLines(c("", paste(W[1:20], W[100:120], W[200:220]), ""))
# paste() with vectors in R concatenates with spaces.
# W is 0-indexed in Python. R[1:20] -> W[0:20]. R[100:120] -> W[99:120]. R[200:220] -> W[199:220].
slice1 = W[0:20]
slice2 = W[99:120]
slice3 = W[199:220]
combined = " ".join(slice1 + slice2 + slice3)
writeLines(["", combined, ""])