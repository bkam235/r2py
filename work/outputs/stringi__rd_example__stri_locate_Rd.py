import re
import numpy as np
import pandas as pd
import unicodedata

# r2py:entity:stri_locate_all_fixed
def stri_locate_all_fixed(str_val, pattern, omit_no_match=False, get_length=False, case_insensitive=False, overlap=False):
    str_list = [str_val] if isinstance(str_val, str) else (str_val if str_val is not None else [])
    results = []
    
    for s in str_list:
        if s is None or (isinstance(s, float) and np.isnan(s)):
            results.append(np.full((1, 2), np.nan))
            continue
            
        flags = re.IGNORECASE if case_insensitive else 0
        esc_pat = re.escape(pattern)
        
        matches = []
        start_idx = 0
        while start_idx <= len(s):
            match = re.search(esc_pat, s[start_idx:], flags=flags)
            if not match:
                break
            
            abs_start = start_idx + match.start()
            abs_end = start_idx + match.end()
            
            start_pos = abs_start + 1
            end_pos = abs_end
            
            if get_length:
                matches.append([start_pos, end_pos - start_pos + 1])
            else:
                matches.append([start_pos, end_pos])
            
            if overlap:
                start_idx = abs_start + 1
            else:
                start_idx = abs_end
            
            if pattern == "" and not overlap:
                break
        
        if not matches:
            if omit_no_match:
                results.append(np.array([]).reshape(0, 2))
            else:
                results.append(np.full((1, 2), np.nan))
        else:
            results.append(np.array(matches))
            
    return results

# r2py:entity:stri_locate_all_regex
def stri_locate_all_regex(str_val, pattern, omit_no_match=False, capture_groups=False, get_length=False):
    str_list = [str_val] if isinstance(str_val, str) else (str_val if str_val is not None else [])
    results = []
    
    for s in str_list:
        if s is None or (isinstance(s, float) and np.isnan(s)):
            res = np.full((1, 2), np.nan)
            if capture_groups:
                regex_obj = re.compile(pattern)
                num_groups = regex_obj.groups
                group_names = regex_obj.groupindex
                all_group_identifiers = [group_names.get(i, str(i)) if group_names else str(i) for i in range(1, num_groups + 1)]
                group_results = {name: np.full((1, 2), np.nan) for name in all_group_identifiers}
                results.append((res, group_results))
            else:
                results.append(res)
            continue
            
        matches_all = list(re.finditer(pattern, s))
        
        if not matches_all:
            res = np.full((1, 2), np.nan)
            if omit_no_match:
                res = np.array([]).reshape(0, 2)
            if capture_groups:
                regex_obj = re.compile(pattern)
                num_groups = regex_obj.groups
                group_names = regex_obj.groupindex
                all_group_identifiers = [group_names.get(i, str(i)) if group_names else str(i) for i in range(1, num_groups + 1)]
                group_results = {name: np.full((1, 2), np.nan) for name in all_group_identifiers}
                results.append((res, group_results))
            else:
                results.append(res)
            continue
        
        main_res = []
        for m in matches_all:
            start = m.start() + 1
            end = m.end()
            if get_length:
                main_res.append([start, end - start + 1])
            else:
                main_res.append([start, end])
        
        main_res = np.array(main_res)
            
        if capture_groups:
            regex_obj = re.compile(pattern)
            num_groups = regex_obj.groups
            group_names = regex_obj.groupindex
            all_group_identifiers = [group_names.get(i, str(i)) if group_names else str(i) for i in range(1, num_groups + 1)]
            
            final_groups = {}
            for i in range(1, num_groups + 1):
                name = all_group_identifiers[i-1]
                g_matches = []
                for m in matches_all:
                    span = m.span(i)
                    if span[0] == -1:
                        g_matches.append([np.nan, np.nan])
                    else:
                        s_start, e_end = span
                        start_pos = s_start + 1
                        end_pos = e_end
                        if get_length:
                            g_matches.append([start_pos, end_pos - start_pos + 1])
                        else:
                            g_matches.append([start_pos, end_pos])
                final_groups[name] = np.array(g_matches)
            results.append((main_res, final_groups))
        else:
            results.append(main_res)
            
    return results

# r2py:entity:stri_locate_first_fixed
def stri_locate_first_fixed(str_val, pattern, get_length=False):
    str_list = [str_val] if isinstance(str_val, str) else (str_val if str_val is not None else [])
    results = []
    for s in str_list:
        if s is None or (isinstance(s, float) and np.isnan(s)):
            results.append(np.full((1, 2), np.nan))
            continue
        idx = s.find(pattern)
        if idx == -1:
            # R returns -1 -1 for some first_fixed misses when get_length=T
            if get_length:
                results.append(np.full((1, 2), -1))
            else:
                results.append(np.full((1, 2), np.nan))
        else:
            start = idx + 1
            end = idx + len(pattern)
            res = np.array([[start, end - start + 1] if get_length else [start, end]])
            results.append(res)
    return results

# r2py:entity:stri_locate_last_fixed
def stri_locate_last_fixed(str_val, pattern, get_length=False):
    str_list = [str_val] if isinstance(str_val, str) else (str_val if str_val is not None else [])
    results = []
    for s in str_list:
        if s is None or (isinstance(s, float) and np.isnan(s)):
            results.append(np.full((1, 2), np.nan))
            continue
        idx = s.rfind(pattern)
        if idx == -1:
            results.append(np.full((1, 2), np.nan))
        else:
            start = idx + 1
            end = idx + len(pattern)
            res = np.array([[start, end - start + 1] if get_length else [start, end]])
            results.append(res)
    return results

# r2py:entity:stri_locate_last_regex
def stri_locate_last_regex(str_val, pattern, capture_groups=False, get_length=False):
    str_list = [str_val] if isinstance(str_val, str) else (str_val if str_val is not None else [])
    results = []
    for s in str_list:
        if s is None or (isinstance(s, float) and np.isnan(s)):
            results.append(np.full((1, 2), np.nan))
            continue
        matches = list(re.finditer(pattern, s))
        if not matches:
            results.append(np.full((1, 2), np.nan))
        else:
            m = matches[-1]
            start = m.start() + 1
            end = m.end()
            res = np.array([[start, end - start + 1] if get_length else [start, end]])
            results.append(res)
    return results

# r2py:entity:stri_locate_first_coll
def stri_locate_first_coll(str_val, pattern, strength=1, locale='sk_SK'):
    def normalize_str(text):
        return "".join(c for c in unicodedata.normalize('NFD', text.casefold()) 
                      if unicodedata.category(c) != 'Mn')

    s_norm = normalize_str(str_val)
    p_norm = normalize_str(pattern)
    
    idx = s_norm.find(p_norm)
    if idx == -1:
        return np.full((1, 2), np.nan)
    return np.array([[idx + 1, idx + len(pattern)]])

# r2py:entity:stri_locate_all
def stri_locate_all(str_val, regex=None, fixed=None, coll=None, charclass=None):
    if fixed:
        return stri_locate_all_fixed(str_val, fixed)
    if regex:
        return stri_locate_all_regex(str_val, regex)
    raise ValueError("Specify regex, fixed, coll, or charclass")

# --- Example Execution ---

# r2py:entity:stri_locate_all
print(stri_locate_all('stringi', fixed='i'))

# r2py:entity:stri_locate_first_coll
print(stri_locate_first_coll('hladn\u00FD', 'HLADNY', strength=1, locale='sk_SK'))

# r2py:entity:stri_locate_all_regex
print(stri_locate_all_regex(
    ['breakfast=eggs;lunch=pizza', 'breakfast=spam', 'no food here'],
    r'(?P<when>\w+)=(?P<what>\w+)',
    capture_groups=True
))

# r2py:entity:stri_locate_all_fixed
print(stri_locate_all_fixed("abababa", "ABA", case_insensitive=True, overlap=True))
# r2py:entity:stri_locate_first_fixed
print(stri_locate_first_fixed("ababa", "aba"))
# r2py:entity:stri_locate_last_fixed
print(stri_locate_last_fixed("ababa", "aba"))
# r2py:entity:stri_locate_last_regex
print(stri_locate_last_regex("ababa", "aba"))

# r2py:entity:x
x = ["yes yes", "no", np.nan]
# r2py:entity:stri_locate_all_fixed_1
print(stri_locate_all_fixed(x, "yes"))
# r2py:entity:stri_locate_all_fixed_2
print(stri_locate_all_fixed(x, "yes", omit_no_match=True))
# r2py:entity:stri_locate_all_fixed_3
print(stri_locate_all_fixed(x, "yes", get_length=True))
# r2py:entity:stri_locate_all_fixed_4
print(stri_locate_all_fixed(x, "yes", get_length=True, omit_no_match=True))
# r2py:entity:stri_locate_first_fixed_1
print(stri_locate_first_fixed(x, "yes"))
# r2py:entity:stri_locate_first_fixed_2
print(stri_locate_first_fixed(x, "yes", get_length=True))

# Use regex positive-lookahead to locate overlapping pattern matches:
# r2py:entity:stri_locate_all_regex_1
print(stri_locate_all_regex('ACAGAGACTTTAGATAGAGAAGA', r'(?=AGA)'))