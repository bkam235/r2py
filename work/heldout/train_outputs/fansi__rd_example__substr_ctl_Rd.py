# Translated from <R script> by r2py v0.3.0

# r2py:data_shim:begin
# import json as _r2py_shim_json
# from pathlib import Path as _r2py_shim_Path
# if '__file__' not in globals(): __file__ = 'work/heldout/train_outputs/fansi__rd_example__substr_ctl_Rd.py'
# _r2py_shim_data = _r2py_shim_json.loads((_r2py_shim_Path(__file__).parent / 'fansi__rd_example__substr_ctl_Rd.r2py_data.json').read_text(encoding='utf-8'))
# for _r2py_shim_n in ['x', 'x1', 'x2', 'x3']:
#     if _r2py_shim_n in _r2py_shim_data:
#         globals()[_r2py_shim_n] = _r2py_shim_data[_r2py_shim_n]
# r2py:data_shim:end

import re
import unicodedata

def get_ansi_parts(s):
    # ANSI escape sequences
    ansi_pattern = re.compile(r'(\033\[[0-9;]*[mK])')
    return ansi_pattern.split(s)

def get_char_width(char):
    return 2 if unicodedata.east_asian_width(char) in ('W', 'F') else 1

# r2py:entity:substr2_ctl
def substr2_ctl(x, start, stop, type_val="chars", round_val="start", tabs_as_spaces=False, tab_stops=8, warn=True, term_cap=None, ctl="all", normalize=False, carry=False, terminate=True):
    if isinstance(x, list):
        results = []
        current_carry_sgr = ""
        for item in x:
            effective_carry = carry
            if carry is True:
                effective_carry = current_carry_sgr
            
            res = substr2_ctl(item, start, stop, type_val, round_val, tabs_as_spaces, tab_stops, warn, term_cap, ctl, normalize, effective_carry, terminate)
            
            parts = get_ansi_parts(item)
            for p in reversed(parts):
                if p.startswith('\033[') and p.endswith('m'):
                    current_carry_sgr = p
                    break
            results.append(res)
        return results

    parts = get_ansi_parts(x)
    logical_chars = []
    char_to_part_idx = []
    
    for i, part in enumerate(parts):
        if not (part.startswith('\033[') and (part.endswith('m') or part.endswith('K'))):
            for char in part:
                logical_chars.append(char)
                char_to_part_idx.append(i)

    if type_val == "width":
        visual_positions = [0]
        for char in logical_chars:
            visual_positions.append(visual_positions[-1] + get_char_width(char))
        
        v_start = start - 1
        v_stop = stop - 1
        
        def map_visual_to_logical(v, mode):
            if v < 0: return 0
            if v >= len(visual_positions): return len(logical_chars)
            for i in range(len(visual_positions) - 1):
                if visual_positions[i] <= v < visual_positions[i+1]:
                    width = visual_positions[i+1] - visual_positions[i]
                    if width == 2 and v == visual_positions[i] + 1:
                        if mode == 'start': return i 
                        if mode == 'stop': return i + 1 
                        if mode == 'neither': return i 
                        if mode == 'both': return i 
                    return i
            return len(logical_chars)

        l_start = map_visual_to_logical(v_start, round_val)
        l_stop = map_visual_to_logical(v_stop, round_val)
        
        if round_val == 'both':
            if 0 < v_start < len(visual_positions) and (visual_positions[l_start] + 1 == v_start) and get_char_width(logical_chars[l_start]) == 2:
                l_start -= 1
            if 0 < v_stop < len(visual_positions) and (visual_positions[l_stop] + 1 == v_stop) and get_char_width(logical_chars[l_stop]) == 2:
                l_stop += 1
    else:
        l_start = start - 1
        l_stop = stop

    l_start = max(0, min(l_start, len(logical_chars)))
    l_stop = max(0, min(l_stop, len(logical_chars)))

    active_sgr = ""
    if isinstance(carry, str) and carry:
        active_sgr = carry
    elif l_start < len(char_to_part_idx):
        p_idx = char_to_part_idx[l_start]
        for i in range(p_idx, -1, -1):
            if parts[i].startswith('\033[') and parts[i].endswith('m'):
                active_sgr = parts[i]
                break
    else:
        for i in range(len(parts)-1, -1, -1):
            if parts[i].startswith('\033[') and parts[i].endswith('m'):
                active_sgr = parts[i]
                break

    res = active_sgr
    current_logical_idx = 0
    for i, part in enumerate(parts):
        if not (part.startswith('\033[') and (part.endswith('m') or part.endswith('K'))):
            for char in part:
                if l_start <= current_logical_idx < l_stop:
                    res += char
                current_logical_idx += 1
        else:
            if l_start < current_logical_idx < l_stop:
                res += part

    if terminate and active_sgr:
        if not (res.endswith('\033[0m') or res.endswith('\033[m')):
            res += '\033[0m'
            
    if not terminate:
        if stop > len(logical_chars):
            for i in range(len(parts)-1, -1, -1):
                if parts[i].startswith('\033['):
                    res += parts[i]
                    break
                    
    return res

# r2py:entity:substr_ctl
def substr_ctl(x, start, stop, warn=True, term_cap=None, ctl="all", normalize=False, carry=False, terminate=True):
    return substr2_ctl(x, start, stop, type_val="chars", warn=warn, term_cap=term_cap, ctl=ctl, normalize=normalize, carry=carry, terminate=terminate)

# r2py:entity:writeLines
def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# r2py:entity:substr_ctl(x1, 2, 2)
def substr_ctl_replace(x_in, start, stop, value, carry=False):
    if not isinstance(x_in, list):
        x_in = [x_in]
    
    results = []
    for s in x_in:
        parts = get_ansi_parts(s)
        logical_chars = []
        char_to_part_idx = []
        for i, part in enumerate(parts):
            if not (part.startswith('\033[') and (part.endswith('m') or part.endswith('K'))):
                for char in part:
                    logical_chars.append(char)
                    char_to_part_idx.append(i)
        
        l_start = max(0, start - 1)
        l_stop = max(0, stop)
        
        prefix_logical = "".join(logical_chars[:l_start])
        suffix_logical = "".join(logical_chars[l_stop:])
        
        sgr_at_start = ""
        if l_start < len(char_to_part_idx):
            idx = char_to_part_idx[l_start]
            for i in range(idx, -1, -1):
                if parts[i].startswith('\033[') and parts[i].endswith('m'):
                    sgr_at_start = parts[i]
                    break
        
        if carry is True:
            # carry=True preserves original SGR exactly around the replacement
            res = f"{sgr_at_start}{prefix_logical}\033[0m{value}{sgr_at_start}{suffix_logical}"
        else:
            res = f"{sgr_at_start}{prefix_logical}\033[0m{value}{sgr_at_start}{suffix_logical}"
            
        if value.startswith('\033['):
            res = res.replace('\033[0m' + value, value)

        results.append(res)
    return results

def format_r_out(val):
    if isinstance(val, list):
        return '[1] "' + '" "'.join(val) + '"'
    return f'[1] "{val}"'

# r2py:entity:substr_ctl
print(format_r_out(substr_ctl("\033[42mhello\033[m world", 1, 9)))
# r2py:entity:substr_ctl_1
print(format_r_out(substr_ctl("\033[42mhello\033[m world", 3, 9)))

# R: x (implicitly prints)
# x is "\uFF37n\uFF37"
# r2py:entity:x
x = "\uFF37n\uFF37" 
# R output: [1] "ＷnＷ"
# r2py:entity:x_1
print(format_r_out(x))
# r2py:entity:substr2_ctl
print(format_r_out(substr2_ctl(x, 2, 4, type_val='width', round_val='start')))
# r2py:entity:substr2_ctl_1
print(format_r_out(substr2_ctl(x, 2, 4, type_val='width', round_val='stop')))
# r2py:entity:substr2_ctl_2
print(format_r_out(substr2_ctl(x, 2, 4, type_val='width', round_val='neither')))
# r2py:entity:substr2_ctl_3
print(format_r_out(substr2_ctl(x, 2, 4, type_val='width', round_val='both')))

# r2py:entity:substr_ctl_2
print(format_r_out(substr_ctl("\033[31mhello\tworld", 1, 6, ctl='sgr', warn=False)))
# r2py:entity:substr_ctl_3
print(format_r_out(substr_ctl("\033[31mhello\tworld", 1, 6, ctl=['all', 'c0'], warn=False)))

# r2py:entity:substr_ctl_4
print(format_r_out(substr_ctl(["\033[33mhello", "world"], 1, 3)))
# r2py:entity:substr_ctl_5
print(format_r_out(substr_ctl(["\033[33mhello", "world"], 1, 3, carry=True)))
# r2py:entity:substr_ctl_6
print(format_r_out(substr_ctl(["\033[33mhello", "world"], 1, 3, carry="\033[44m")))

# r2py:entity:bleed
bleed = substr_ctl(["\033[41mhello", "world"], 1, 3, terminate=False)
# r2py:entity:writeLines
writeLines(bleed)
# r2py:entity:end
end = "\033[0m\n"
# r2py:entity:writeLines_1
writeLines(end)

# r2py:entity:substr_ctl_7
print(format_r_out(substr_ctl("ABC\033[42m", 1, 3, terminate=False)))
# r2py:entity:substr_ctl_8
print(format_r_out(substr_ctl("ABC\033[42m", 1, 4, terminate=False)))

# r2py:entity:c
x0 = x1 = x2 = x3 = ["\033[42mABC", "\033[34mDEF"]
# r2py:entity:substr_ctl(x1, 2, 2)
x1 = substr_ctl_replace(x1, 2, 2, "_")
# r2py:entity:substr_ctl(x2, 2, 2)
x2 = substr_ctl_replace(x2, 2, 2, "\033[m_")
# r2py:entity:substr_ctl(x3, 2, 2)
x3 = substr_ctl_replace(x3, 2, 2, "\033[45m_")
# r2py:entity:writeLines_2
writeLines(x0 + [end] + x1 + [end] + x2 + [end] + x3 + [end])

# r2py:entity:x2_1
x0 = x1 = x2 = x3 = ["\033[42mABC", "\033[34mDEF"]
# r2py:entity:substr_ctl(x0, 2, 2, carry=TRUE)
x0 = substr_ctl_replace(x0, 2, 2, "_", carry=True)
# r2py:entity:substr_ctl(x1, 2, 2, carry=TRUE)
x1 = substr_ctl_replace(x1, 2, 2, "\033[m_", carry=True)
# r2py:entity:substr_ctl(x2, 2, 2, carry=TRUE)
x2 = substr_ctl_replace(x2, 2, 2, "\033[45m_", carry=True)
# r2py:entity:writeLines_3
writeLines(x0 + [end] + x1 + [end] + x2 + [end] + x3 + [end])

# r2py:entity:x_2
x = ["ABC", "DEF"]
# r2py:entity:val
val = "#"
# r2py:entity:x2_2
x2 = ["\033[42m"] + x
# r2py:entity:val2
val2 = ["\033[45m"] + [val] * len(x)

# r2py:entity:substr_ctl(x2, 2, 2, carry=TRUE)_1
def substr_ctl_replace_vec(x_vec, start, stop, values, carry=False):
    results = []
    for i in range(len(x_vec)):
        s = x_vec[i]
        if i == 0 and s.startswith('\033['):
            results.append(s)
            continue
        v = values[i] if i < len(values) else values[-1]
        res = substr_ctl_replace([s], start, stop, v, carry)[0]
        results.append(res)
    return results

x2 = substr_ctl_replace_vec(x2, 2, 2, val2, carry=True)
# r2py:entity:x_3
x = x[1:] # R's x[-1]
print(format_r_out(x))