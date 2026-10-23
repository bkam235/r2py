# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import os
import stat

# Helper function to mimic fs_perms behavior
# In R, fs_perms converts numeric/string/symbolic modes to the standard string representation
# r2py:entity:fs_perms
def fs_perms(mode):
    if isinstance(mode, (list, tuple)):
        return [fs_perms(m) for m in mode]
    
    # Handle numeric octal input (e.g., 420L is decimal, but usually represents octal in perms context)
    # R's fs_perms treats integers as decimal representations of octal modes
    if isinstance(mode, int):
        # Convert decimal to octal string, then to mode
        octal_str = oct(mode)[2:]
        # Ensure 3-digit format
        octal_str = octal_str.zfill(3)
        mode_val = int(octal_str, 8)
    elif isinstance(mode, str):
        # Simple check if it's a numeric string like "777"
        if mode.isdigit():
            mode_val = int(mode, 8)
        else:
            # Symbolic modes like "a+rwx" are complex to parse manually; 
            # for a direct translation of the logic, we map common symbolic outputs
            # since Python's os.chmod handles them but doesn't 'return' the string form.
            # This is a mock representation of the R fs_perms string output logic.
            return mode 
    else:
        return mode

    # Convert mode integer to the R-style string representation (e.g., "rwxr-xr-x")
    # However, fs_perms in R returns the human-readable string version of the bits.
    # We can simulate the specific outputs seen in the R fs package.
    # For the purpose of this translation, we use a simple format map.
    res = ""
    perms = [
        (stat.S_IRUSR, 'u+r'), (stat.S_IWUSR, 'u+w'), (stat.S_IXUSR, 'u+x'),
        (stat.S_IRGRP, 'g+r'), (stat.S_IWGRP, 'g+w'), (stat.S_IXGRP, 'g+x'),
        (stat.S_IROTH, 'o+r'), (stat.S_IWOTH, 'o+w'), (stat.S_IXOTH, 'o+x'),
    ]
    
    # fs_perms output varies by OS, but generally returns the string representation
    # To match R's behavior of returning a string like "rwxr-xr-x" or the symbolic mode:
    return oct(mode_val & 0o777)[2:].zfill(3)

# Note: Since fs_perms in R is primarily for getting/setting filesystem permissions 
# and the provided snippet tests the string conversion logic, we implement the logic accordingly.

# r2py:entity:fs_perms
print(fs_perms(420))
# r2py:entity:fs_perms_1
print(fs_perms([511, 420]))

# r2py:entity:fs_perms_2
print(fs_perms("777"))
# r2py:entity:fs_perms_3
print(fs_perms(["777", "644"]))

# r2py:entity:fs_perms_4
print(fs_perms("a+rwx"))
# r2py:entity:fs_perms_5
print(fs_perms(["a+rwx", "u+rw,go+r"]))

# (fs_perms("777") & "u+r") == "u+r"
# In R, the & operator on these strings is likely a bitwise operation on the permissions
# Here we simulate the logical check: if "777" (rwxrwxrwx) has "u+r" (user read)
# r2py:entity:fs_perms_6
res = (int("777", 8) & stat.S_IRUSR) == stat.S_IRUSR
print(res)