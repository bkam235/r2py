# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import re

# r2py:entity:str
def col_red(text):
    """Wraps text in ANSI red color codes."""
    return f"\033[31m{text}\033[39m"

def col_green(text):
    """Wraps text in ANSI green color codes."""
    return f"\033[32m{text}\033[39m"

def style_underline(text):
    """Wraps text in ANSI underline codes."""
    return f"\033[4m{text}\033[24m"

# r2py:entity:strsplit_1
def ansi_strip(text):
    """Removes ANSI escape sequences from a string."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[JKmn])')
    return ansi_escape.sub('', text)

# r2py:entity:cat_1
def ansi_strsplit(text, pattern):
    """
    Splits a string by a pattern while preserving ANSI escape sequences.
    Mimics cli::ansi_strsplit.
    """
    if pattern == "":
        return [list(text)]
    
    # Find positions of delimiters in the stripped (plain) text
    plain_text = ansi_strip(text)
    matches = list(re.finditer(pattern, plain_text))
    
    # Map plain text indices back to original text indices
    # by iterating through the original and tracking ANSI sequences
    mapping = []
    current_plain_idx = 0
    in_ansi = False
    for i, char in enumerate(text):
        if not in_ansi and char == '\x1b':
            in_ansi = True
            continue
        if in_ansi:
            if char == 'm' or char == 'K' or char == 'J': # Simplified ANSI end check
                in_ansi = False
            continue
        mapping.append(i)
        current_plain_idx += 1

    # Split points in the original string
    split_indices = []
    for match in matches:
        start = mapping[match.start()]
        end = mapping[match.end() - 1] + 1 if match.end() <= len(mapping) else len(text)
        split_indices.append((start, end))

    # Extract chunks between delimiters
    chunks = []
    last_end = 0
    for start, end in split_indices:
        chunks.append(text[last_end:start])
        last_end = end
    chunks.append(text[last_end:])
    
    return [chunks]

# --- Example Execution ---

# r2py:entity:str
str_val = (
    col_red("I am red---") + 
    col_green("and I am green-") + 
    style_underline("I underlined")
)

# r2py:entity:cat
print(str_val)
print()

# split at dashes, keep color
# r2py:entity:cat_1
split_result = ansi_strsplit(str_val, "[-]+")[0]
for item in split_result:
    print(item)

# Translate strsplit(ansi_strip(str), "[-]+")
# r2py:entity:strsplit
print(re.split("[-]+", ansi_strip(str_val)))

# split to characters, keep color
# r2py:entity:cat_2
char_split = ansi_strsplit(str_val, "")[0]
print(" ".join(char_split))
print()

# Translate strsplit(ansi_strip(str), "")
# r2py:entity:strsplit_1
print(list(ansi_strip(str_val)))