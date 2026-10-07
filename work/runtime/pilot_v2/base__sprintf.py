import numpy as np
import pandas as pd

def r_sprintf(*args, **kwargs):
    """
    Reproduces R's sprintf function.
    R's sprintf handles NA by converting it to the literal string "NA" 
    regardless of the format specifier (e.g., %f, %d).
    """
    # Extract fmt: it is either the first positional argument or a keyword argument 'fmt'
    if 'fmt' in kwargs:
        fmt = kwargs.pop('fmt')
        vals = args
    elif len(args) > 0:
        fmt = args[0]
        vals = args[1:]
    else:
        return ""

    # R ignores unused arguments in the ... ellipsis that don't match format specifiers
    # Python's % operator will throw an error if too many args are provided.
    # However, R's sprintf behavior is to use the args required by fmt.
    
    # Convert positional arguments to numpy arrays to handle recycling.
    inputs = []
    for arg in vals:
        # Convert to numpy array and ensure we handle scalars correctly
        arr = np.atleast_1d(arg)
        inputs.append(arr)
    
    if not inputs:
        # If no values provided, return fmt as a scalar if it's a scalar
        return fmt if isinstance(fmt, str) else list(fmt)

    # Determine the length of the output vector (recycling)
    lengths = [arr.size for arr in inputs]
    max_len = max(lengths) if lengths else 1
    
    # Identify how many arguments the format string actually expects
    # This is a simplification; real R sprintf uses the C-style parser.
    import re
    placeholders = re.findall(r'%[0-9.]*[-+ #0]*[hljstdefgS]', fmt)
    num_expected = len(placeholders)
    
    results = []
    for i in range(max_len):
        current_vals = []
        # We only take the first 'num_expected' arguments from the recycled list
        for j in range(num_expected):
            if j >= len(inputs):
                # This case is rare in R as it would usually throw an error 
                # if too few arguments are provided for the format string.
                break
            
            arr = inputs[j]
            val = arr[i % arr.size]
            
            # R's sprintf replaces NA with "NA" literally, even for %f or %d.
            # If we pass "NA" to Python's %f, it raises a TypeError.
            # We must detect the NA and manually handle the substitution.
            if pd.isna(val) if not isinstance(val, str) else False:
                current_vals.append("NA")
            else:
                current_vals.append(val)
        
        # To mimic R, if any value is "NA", we must bypass the Python type check 
        # for that specific placeholder. 
        # We do this by splitting the format string or using a custom formatter.
        
        temp_fmt = fmt
        temp_vals = list(current_vals)
        
        # Because Python's % operator doesn't allow "NA" for %f, 
        # we replace the specific format specifier with %s if the value is "NA".
        # This is a bit complex, so we'll iterate through the placeholders.
        
        final_str = ""
        last_pos = 0
        val_idx = 0
        
        # Simple regex to find all % specifiers
        for match in re.finditer(r'%[0-9.]*[-+ #0]*[hljstdefgS]', fmt):
            final_str += fmt[last_pos:match.start()]
            spec = match.group()
            
            if val_idx < len(temp_vals):
                val = temp_vals[val_idx]
                if val == "NA":
                    # Replace the specifier with %s to allow the string "NA"
                    final_str += "%s" % "NA"
                else:
                    # Use the original specifier
                    final_str += spec % val
                val_idx += 1
            else:
                final_str += spec # Keep the specifier if no value
            
            last_pos = match.end()
        
        final_str += fmt[last_pos:]
        results.append(final_str)

    if max_len == 1:
        return results[0]
    else:
        return results
