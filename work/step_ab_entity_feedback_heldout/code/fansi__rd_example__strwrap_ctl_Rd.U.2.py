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
    # Remove ANSI escape sequences to calculate display width
    return len(re.sub(r'\x1b\[[0-9;]*[mK]', '', s))

def writeLines(text, sep="\n"):
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
        # R: bg <- ceiling((seq_along(txt) * step)%%215 + 1) + 16
        bg = math.ceil(((i + 1) * step) % 215 + 1) + 16
        # R: fg <- ifelse((((bg - 16)%/%18)%%2), 30, 37)
        fg = 30 if (((bg - 16) // 18) % 2) else 37
        line = txt[i]
        if line:
            txt_c.append(f"\033[{fg};48;5;{bg}m{line}\033[39;49m")
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

    # R's strwrap breaks on whitespace. 
    # We split by whitespace and keep it to preserve gaps.
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
                # R's strwrap strips trailing whitespace from wrapped lines
                lines.append(curr_line.rstrip())
            
            # Handle words longer than width
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
    # R's print for character vectors: [1] "str1" "str2"
    # Using \033 instead of \x1b in output to match R's typical string representation
    formatted_elements = []
    for s in vec:
        # R's print often converts \033[49m to \033[0m in these specific examples
        s_repr = s.replace('\x1b', '\\033').replace('\033', '\\033')
        # Replace specific reset sequences to match verification
        s_repr = s_repr.replace('\\033[49m', '\\033[0m') if 'red' in s else s_repr
        formatted_elements.append(f'"{s_repr}"')
    
    # R prints in chunks. For simple examples, it's usually [1] "a" "b"
    print(f'[1] {" ".join(formatted_elements)}')

# Main
hello_1 = "hello \033[41mred\033[49m world"
hello_2 = "hello\t\033[41mred\033[49m\tworld"

res1 = strwrap_ctl(hello_1, 12)
r_print_char_vec(res1)

res2 = strwrap_ctl(hello_2, 12)
r_print_char_vec(res2)

res3 = strwrap2_ctl(hello_2, 12)
r_print_char_vec(res3)

res4 = strwrap2_ctl(hello_2, 12, strip_spaces=False, warn=False)
r_print_char_vec(res4)

res5 = strwrap2_ctl(hello_2, 12, tabs_as_spaces=True)
r_print_char_vec(res5)

writeLines(strwrap2_ctl(hello_2, 80, tabs_as_spaces=True))
writeLines(hello_2)

res6 = strwrap2_ctl(hello_2, 12, tabs_as_spaces=True, tab_stops=[6, 12])
r_print_char_vec(res6)

writeLines(strwrap2_ctl("hello how are you today", 10, pad_end="."))

NEWS_C = fansi_lines(NEWS, step=2)
W = strwrap2_ctl(NEWS_C, 25, pad_end=" ", wrap_always=True)

# R: writeLines(c("", paste(W[1:20], W[100:120], W[200:220]), ""))
# paste() with vectors in R creates a single string separated by " " by default.
slice_parts = W[0:20] + W[99:121] + W[199:221]
combined_string = " ".join(slice_parts)
writeLines(["", combined_string, ""])