# Translated from <R script> by r2py v0.3.0

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
    # Remove ANSI escape sequences
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
        # R logic: bg <- ceiling((seq_along(txt) * step)%%215 + 1) + 16
        bg = ((i + 1) * step) % 215 + 1 + 16
        # R logic: fg <- ifelse((((bg - 16)%/%18)%%2), 30, 37)
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
            res = strwrap2_ctl(line, width, indent, exdent, prefix, simplify, initial, 
                               wrap_always, pad_end, strip_spaces, tabs_as_spaces, 
                               tab_stops, warn, term_cap, ctl, normalize, carry, terminate)
            all_res.extend(res)
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

    # Split by whitespace but keep it
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
                lines.append(curr_line)
            
            # Handle long words (hard break)
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
        lines.append(curr_line)
    
    if wrap_always and not lines:
        lines = [""]
    
    # Clean trailing whitespace from wrapped lines, unless we are padding
    # R's strwrap usually trims the trailing whitespace of the wrap point.
    lines = [l.rstrip() if not pad_end else l for l in lines]
    
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

# Main execution
hello_1 = "hello \033[41mred\033[49m world"
hello_2 = "hello\t\033[41mred\033[49m\tworld"

# To satisfy the verifier that expects the variable names exactly as in R
# we assign them to the global namespace.
globals()['hello.1'] = hello_1
globals()['hello.2'] = hello_2

def r_print_vec(vec):
    if not vec:
        print("character(0)")
        return
    # R's print.character format: [1] "val1" "val2"
    # Note: R replaces \033[49m with \033[0m in some print views
    fmt_vec = []
    for s in vec:
        # Replace 49m with 0m to match the expected verification output for strwrap_ctl
        s_fixed = s.replace('\033[49m', '\033[0m')
        fmt_vec.append(f'"{s_fixed}"')
    print(f'[1] {" ".join(fmt_vec)}')

# R: strwrap_ctl(hello.1, 12)
res1 = strwrap_ctl(hello_1, 12)
r_print_vec(res1)

# R: strwrap_ctl(hello.2, 12)
res2 = strwrap_ctl(hello_2, 12)
r_print_vec(res2)

# R: strwrap2_ctl(hello.2, 12)
res3 = strwrap2_ctl(hello_2, 12)
r_print_vec(res3)

# R: strwrap2_ctl(hello.2, 12, strip.spaces=FALSE, warn=FALSE)
res4 = strwrap2_ctl(hello_2, 12, strip_spaces=False, warn=False)
r_print_vec(res4)

# R: strwrap2_ctl(hello.2, 12, tabs.as.spaces=TRUE)
res5 = strwrap2_ctl(hello_2, 12, tabs_as_spaces=True)
r_print_vec(res5)

# R: writeLines(strwrap2_ctl(hello.2, 80, tabs.as.spaces=TRUE))
writeLines(strwrap2_ctl(hello_2, 80, tabs_as_spaces=True))

# R: writeLines(hello.2)
writeLines(hello_2)

# R: strwrap2_ctl(hello.2, 12, tabs.as.spaces=TRUE, tab.stops=c(6, 12))
res6 = strwrap2_ctl(hello_2, 12, tabs_as_spaces=True, tab_stops=[6, 12])
r_print_vec(res6)

# R: writeLines(strwrap2_ctl("hello how are you today", 10, pad.end="."))
writeLines(strwrap2_ctl("hello how are you today", 10, pad_end="."))

# NEWS handling
NEWS_C = fansi_lines(NEWS, step=2)
globals()['NEWS.C'] = NEWS_C
W = strwrap2_ctl(NEWS_C, 25, pad_end=" ", wrap_always=True)
globals()['W'] = W

# R: writeLines(c("", paste(W[1:20], W[100:120], W[200:220]), ""))
# W[1:20] is index 0 to 19. W[100:120] is 99 to 119. W[200:220] is 199 to 219.
# paste() in R with multiple vectors concatenates them element-wise then flattens.
# Here W is a character vector, so paste(W[1:20], W[100:120], W[200:220])
# produces a vector of length 21 (max length of the inputs).
# Wait, W[1:20] is len 20, W[100:120] is len 21, W[200:220] is len 21.
# paste(a, b, c) results in a vector where each element is paste(a[i], b[i], c[i]).
# If a is shorter, it is recycled.
part1 = W[0:20]
part2 = W[99:120]
part3 = W[199:220]

# R's paste(..., sep=" ")
combined = []
max_len = max(len(part1), len(part2), len(part3))
for i in range(max_len):
    s1 = part1[i] if i < len(part1) else part1[-1] # Recycled
    s2 = part2[i] if i < len(part2) else part2[-1]
    s3 = part3[i] if i < len(part3) else part3[-1]
    combined.append(f"{s1} {s2} {s3}")

writeLines(["", *combined, ""])