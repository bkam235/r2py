import numpy as np
import pandas as pd

def r_format(x, trim=False, digits=None, nsmall=0, justify="left", width=None, 
             na_encode=True, scientific=None, big_mark="", big_interval=3, 
             small_mark="", small_interval=5, decimal_mark=".", 
             zero_print=None, drop0trailing=False, *args, **kwargs):
    
    valid_justifies = ["left", "right", "centre", "none"]
    if justify not in valid_justifies:
        justify = "left"

    if x is None:
        return "NULL"

    # Handle list/DataFrame logic
    if isinstance(x, (list, pd.DataFrame, pd.Series)) and not isinstance(x, np.ndarray):
        if trim is None: trim = True
        if justify == "none" or justify is None: justify = "none"
        res = []
        # Treat as a list of elements
        items = x.values if hasattr(x, 'values') else x
        for item in items:
            val = np.array(item).flatten()
            formatted_vec = r_format(val, trim=True, justify="none", digits=digits, 
                                     nsmall=nsmall, width=width, na_encode=na_encode, 
                                     scientific=scientific, big_mark=big_mark, 
                                     big_interval=big_interval, small_mark=small_mark, 
                                     small_interval=small_interval, decimal_mark=decimal_mark, 
                                     zero_print=zero_print, drop0trailing=drop0trailing)
            res.append(", ".join(formatted_vec if isinstance(formatted_vec, np.ndarray) else [formatted_vec]))
        return np.array(res)

    # Ensure x is a numpy array for processing, but remember if it was a scalar
    is_scalar = np.isscalar(x)
    x_arr = np.atleast_1d(np.array(x))

    # String handling
    if x_arr.dtype.kind in ('U', 'S', 'O') and not np.issubdtype(x_arr.dtype, np.number) and not np.issubdtype(x_arr.dtype, np.bool_):
        adj = valid_justifies.index(justify)
        res = []
        for val in x_arr:
            s = str(val) if not (pd.isna(val) and na_encode) else "NA"
            if width:
                if adj == 0: s = s.ljust(width)
                elif adj == 1: s = s.rjust(width)
                elif adj == 2: s = s.center(width)
            if trim: s = s.strip()
            res.append(s)
        return np.array(res) if not is_scalar else res[0]

    # Numeric/Logical processing
    formatted_raw = []
    for val in x_arr:
        formatted_raw.append(_r_pretty_num(val, digits, nsmall, na_encode, scientific, 
                                            big_mark, big_interval, small_mark, 
                                            small_interval, decimal_mark, zero_print, 
                                            drop0trailing))
    
    # R's numeric format: right-justifies by default (adj=1) for numeric types
    # unless justify is overridden.
    eff_justify = justify if justify != "left" else "right"
    
    if not trim:
        common_width = max(len(s) for s in formatted_raw) if formatted_raw else 0
        if width and width > common_width:
            common_width = width
    else:
        common_width = None

    res = []
    adj = valid_justifies.index(eff_justify)
    for s in formatted_raw:
        if common_width:
            if adj == 0: s = s.ljust(common_width)
            elif adj == 1: s = s.rjust(common_width)
            elif adj == 2: s = s.center(common_width)
        elif trim:
            s = s.strip()
        res.append(s)

    return np.array(res) if not is_scalar else res[0]

def _r_pretty_num(x, digits, nsmall, na_encode, scientific, 
                  big_mark, big_interval, small_mark, small_interval, 
                  decimal_mark, zero_print, drop0trailing):
    
    if pd.isna(x):
        return "NA" if na_encode else ""

    if isinstance(x, (bool, np.bool_)):
        return "TRUE" if x else "FALSE"

    # Use default 7 digits if not specified
    d = digits if digits is not None else 7
    
    # Format using 'g' for significant figures
    s = format(float(x), f'.{d}g')
    
    # Handle scientific notation vs fixed
    if 'e' in s.lower():
        # R keeps the 'e' but we need to apply decimal mark to the mantissa
        parts = s.lower().split('e')
        mantissa = parts[0]
        if '.' in mantissa:
            mantissa = mantissa.replace('.', decimal_mark)
        s = mantissa + 'e' + parts[1]
    else:
        if '.' in s:
            parts = s.split('.')
            dec = parts[1]
            if len(dec) < nsmall:
                s += '0' * (nsmall - len(dec))
            if drop0trailing:
                while s.endswith('0'):
                    s = s[:-1]
                if s.endswith('.'):
                    s = s[:-1]
        elif nsmall > 0:
            s += '.' + '0' * nsmall

        # Replace decimal mark
        if decimal_mark != '.' and '.' in s:
            s = s.replace('.', decimal_mark)

        # Big mark grouping
        if big_mark and big_interval:
            if decimal_mark in s:
                int_part, dec_part = s.split(decimal_mark, 1)
            else:
                int_part, dec_part = s, ""
            
            if int_part.startswith('-'):
                sign, abs_int = '-', int_part[1:]
            else:
                sign, abs_int = '', int_part
                
            groups = []
            while len(abs_int) > big_interval:
                groups.append(abs_int[-big_interval:])
                abs_int = abs_int[:-big_interval]
            groups.append(abs_int)
            s = sign + big_mark.join(reversed(groups)) + (decimal_mark + dec_part if dec_part else "")

    if x == 0 and zero_print is not None:
        s = zero_print
        
    return s
