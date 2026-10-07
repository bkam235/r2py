import numpy as np
import pandas as pd

def r_hms(seconds=None, minutes=None, hours=None, days=None):
    """
    Reproduces hms::hms from R.
    R's hms class stores values as total seconds since midnight.
    Importantly, R's hms representation allows negative values and represents
    them as -HH:MM:SS rather than wrapping around midnight (unlike Python's % operator).
    """
    weights = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400
    }
    
    args = {
        'seconds': seconds,
        'minutes': minutes,
        'hours': hours,
        'days': days
    }
    
    # Determine if input is vector or scalar
    is_vector = False
    for val in args.values():
        if isinstance(val, (list, np.ndarray, pd.Series)):
            is_vector = True
            break
    
    # Calculate total seconds
    total_secs = None
    for key, weight in weights.items():
        val = args[key]
        if val is not None:
            arr = np.array(val, dtype=float)
            term = arr * weight
            if total_secs is None:
                total_secs = term
            else:
                total_secs = total_secs + term
                
    if total_secs is None:
        return np.array([], dtype=float)
    
    # Convert to array for consistent processing
    res_arr = np.atleast_1d(total_secs)
    
    def format_hms(s):
        if np.isnan(s):
            return None
        
        # R's hms formatting for negative values: 
        # It treats the sign separately: - (abs(s) formatted)
        sign = ""
        if s < 0:
            sign = "-"
            s = abs(s)
        
        # Calculate components
        # R's hms does not wrap days into 24h for the purpose of the internal value
        # but the printer typically does. However, the failing cases show 
        # that it preserves the negative sign.
        h = int(s // 3600)
        m = int((s % 3600) // 60)
        sec = s % 60
        
        # Format seconds part
        if sec == int(sec):
            sec_str = f"{int(sec):02d}"
        else:
            # R's hms uses a specific precision for fractional seconds
            # We format to 1 or more decimals as required by the test cases
            sec_str = f"{sec:06.2f}" 
            # Remove trailing zeros but keep at least one decimal if it's a float
            # Based on "00:00:01.1", we should format carefully.
            if sec_str.endswith('0'):
                sec_str = sec_str.rstrip('0').rstrip('.')
            # Ensure it's at least 2 digits before the dot
            # This is complex; let's use a simpler approach for the fraction.
            # R's hms uses `sprintf("%.2f", sec)` effectively but strips trailing zeros.
            # Let's refine:
            sec_val = f"{sec:06.2f}" # e.g. "01.10"
            if sec_val.endswith('0'):
                sec_val = sec_val.rstrip('0').rstrip('.')
            # But hms output for 1.1 is 01.1, not 1.1
            # Re-calculating sec_str for the final return
            parts = f"{sec:06.2f}".split('.')
            whole = parts[0]
            frac = parts[1].rstrip('0').rstrip('.')
            sec_str = whole + ('.' + frac if frac else '')
        
        # The provided "00:00:01.1" suggests HH:MM:S.s
        # Let's rebuild the final string
        if sec == int(sec):
            return f"{sign}{h:02d}:{m:02d}:{int(sec):02d}"
        else:
            # Correct fraction formatting to match R's hms
            # We need 2 digits for whole seconds, then a dot, then decimals.
            # e.g. 1.1 -> 01.1
            whole_sec = int(sec)
            frac_sec = sec - whole_sec
            frac_str = f"{frac_sec:.2f}"[2:].rstrip('0').rstrip('.')
            return f"{sign}{h:02d}:{m:02d}:{whole_sec:02d}.{frac_str}"

    results = [format_hms(x) for x in res_arr]
    
    if not is_vector:
        return results[0]
    else:
        return results
