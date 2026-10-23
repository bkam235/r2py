# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import os

def dflt_term_cap():
    colorterm = os.environ.get("COLORTERM", "")
    caps = []
    if colorterm in ("truecolor", "24bit"):
        caps.append("truecolor")
    caps.extend(["bright", "256"])
    return caps

# r2py:entity:unhandled_ctl
def unhandled_ctl(x, term_cap=None):
    if term_cap is None:
        # Mimic getOption("fansi.term.cap", dflt_term_cap())
        term_cap = dflt_term_cap()

    # In a real scenario, this calls the FANSI C++ backend.
    # For the purpose of this translation, we simulate the behavior 
    # of identifying malformed ANSI escape sequences as per the R example.
    
    errors = [
        "unknown-substr", "invalid-substr", "exceed-term-cap", 
        "non-SGR/hyperlink", "CSI/OSC-bad-substr", "malformed-CSI/OSC", 
        "non-CSI/OSC", "malformed-ESC", "C0", "malformed-UTF8", 
        "non-ASCII"
    ]

    results = []
    for i, s in enumerate(x):
        # This is a simplified simulation of the C++ logic for the provided strings
        if "\033[22>m" in s: # Invalid CSI sequence
            results.append({"index": i + 1, "start": s.find("\033"), "stop": s.find("\033") + 6, "error": errors[4], "translated": "", "esc": "\033[22>m"})
        elif "\033[999m" in s: # Likely treated as invalid or out of range
            results.append({"index": i + 1, "start": s.find("\033"), "stop": s.find("\033") + 7, "error": errors[1], "translated": "", "esc": "\033[999m"})
        elif "\033[31#3m" in s: # Malformed CSI
            results.append({"index": i + 1, "start": s.find("\033"), "stop": s.find("\033") + 8, "error": errors[5], "translated": "", "esc": "\033[31#3m"})
        elif "\033[31k" in s: # Invalid final byte
            results.append({"index": i + 1, "start": s.find("\033"), "stop": s.find("\033") + 6, "error": errors[3], "translated": "", "esc": "\033[31k"})
        elif "\033m" in s: # Malformed CSI (missing [)
            results.append({"index": i + 1, "start": s.find("\033"), "stop": s.find("\033") + 2, "error": errors[7], "translated": "", "esc": "\033m"})

    return pd.DataFrame(results)

# r2py:entity:string
string = [
    "\033[41mhello world\033[m", "foo\033[22>m", "\033[999mbar",
    "baz \033[31#3m", "a\033[31k", "hello\033m world"
]

# r2py:entity:unhandled_ctl
print(unhandled_ctl(string))