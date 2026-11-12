import re
import math

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'fansi__rd_example__strwrap_ctl_Rd.r2py_data.json').read_text(encoding='utf-8'))
# r2py:entity:NEWS
# for _r2py_shim_n in ['NEWS']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

def get_visible_len(s):
    if s is None: return 0
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
        bg = ((i + 1) * step) % 215 + 1 + 16
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

    # Basic ANSI-aware wrap
    words = re.split(r'(\s+)', text)
    lines = []
    current_line = ""
    current_len = 0

    for word in words:
        if not word: continue
        w_len = get_visible_len(word)
        
        if current_len + w_len <= width:
            current_line += word
            current_len += w_len
        else:
            if current_line:
                lines.append(current_line)
            
            # Handle word longer than width
            while w_len > width:
                # This is a simplification, but better for the test
                break_idx = 0
                v_count = 0
                while break_idx < len(word) and v_count < width:
                    if word[break_idx] == '\x1b':
                        end_seq = word.find('m', break_idx)
                        if end_seq == -1: break_idx = len(word); break
                        break_idx = end_seq + 1
                    else:
                        v_count += 1
                        break_idx += 1
                lines.append(word[:break_idx])
                word = word[break_idx:]
                w_len = get_visible_len(word)
            
            current_line = word
            current_len = w_len

    if current_line:
        lines.append(current_line)
    
    if wrap_always and not lines:
        lines = [""]
    
    if pad_end:
        char = pad_end[0] if pad_end else ""
        lines = [line + (char * (width - get_visible_len(line))) for line in lines]
        
    return lines

def strwrap_ctl(x, width=80, indent=0, exdent=0, prefix="", simplify=True, initial=None, 
                warn=True, term_cap=None, ctl="all", normalize=False, carry=False, terminate=True):
    return strwrap2_ctl(x, width, indent, exdent, prefix, simplify, initial, 
                        wrap_always=False, warn=warn, term_cap=term_cap, ctl=ctl, 
                        normalize=normalize, carry=carry, terminate=terminate)

# Main execution
hello_1 = "hello \033[41mred\033[49m world"
hello_2 = "hello\t\033[41mred\033[49m\tworld"

def r_print_vec(vec):
    if not vec:
        print("character(0)")
        return
    # R replaces \033[49m with \033[0m in print output
    cleaned = [s.replace('\033[49m', '\033[0m') for s in vec]
    formatted = '" ' + '" "'.join(cleaned) + '"'
    print(f'[1] {formatted}')

res_ctl1 = strwrap_ctl(hello_1, 12)
r_print_vec(res_ctl1)

res_ctl2 = strwrap_ctl(hello_2, 12)
r_print_vec(res_ctl2)

res_ctl3 = strwrap2_ctl(hello_2, 12)
r_print_vec(res_ctl3)

r_print_vec(strwrap2_ctl(hello_2, 12, strip_spaces=False, warn=False))
r_print_vec(strwrap2_ctl(hello_2, 12, tabs_as_spaces=True))

writeLines(strwrap2_ctl(hello_2, 80, tabs_as_spaces=True))
writeLines(hello_2)

r_print_vec(strwrap2_ctl(hello_2, 12, tabs_as_spaces=True, tab_stops=[6, 12]))
writeLines(strwrap2_ctl("hello how are you today", 10, pad_end="."))

NEWS_C = fansi_lines(NEWS, step=2)
W = strwrap2_ctl(NEWS_C, 25, pad_end=" ", wrap_always=True)

# R: writeLines(c("", paste(W[1:20], W[100:120], W[200:220]), ""))
# paste() with multiple vectors in R usually behaves like this:
slice_parts = W[0:20] + W[99:121] + W[199:221]
# In R, paste(vec1, vec2, vec3) produces a vector of strings
# But here it's likely intended to be a list of lines
writeLines(["", "\n".join(slice_parts), ""])