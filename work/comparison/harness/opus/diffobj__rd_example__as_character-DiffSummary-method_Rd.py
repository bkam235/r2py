# Translated from <R script> by r2py v0.3.0
# Model: claude-opus-4-6  ScriptMap entities: 3

import string
from difflib import SequenceMatcher

# r2py:entity:as.character
letters = list(string.ascii_lowercase)

target = list(string.ascii_lowercase)
current = [ch for i, ch in enumerate(string.ascii_lowercase) if i not in (4, 14)]

# Compute diff statistics
sm = SequenceMatcher(None, target, current)
opcodes = sm.get_opcodes()

num_equal = 0
deleted_count = 0
inserted_count = 0

for tag, i1, i2, j1, j2 in opcodes:
    if tag == 'equal':
        num_equal += (i2 - i1)
    elif tag == 'delete':
        deleted_count += (i2 - i1)
    elif tag == 'insert':
        inserted_count += (j2 - j1)
    elif tag == 'replace':
        deleted_count += (i2 - i1)
        inserted_count += (j2 - j1)

# Build the diff map: '.' for equal chars, 'D' for deletions, 'I' for insertions
diff_map_chars = []
for tag, i1, i2, j1, j2 in opcodes:
    if tag == 'equal':
        diff_map_chars.extend(['.'] * (i2 - i1))
    elif tag == 'delete':
        diff_map_chars.extend(['D'] * (i2 - i1))
    elif tag == 'insert':
        diff_map_chars.extend(['I'] * (j2 - j1))
    elif tag == 'replace':
        diff_map_chars.extend(['D'] * (i2 - i1))
        diff_map_chars.extend(['I'] * (j2 - j1))

diff_map = ''.join(diff_map_chars)

# Count hunks (contiguous non-equal regions)
num_hunks = sum(1 for tag, _, _, _, _ in opcodes if tag != 'equal')

# Build the summary string matching R's diffobj output format
# The string has embedded newlines
summary_str = (
    f"\nFound differences in {num_hunks} hunk{'s' if num_hunks != 1 else ''}:\n"
    f"  {inserted_count} insertion{'s' if inserted_count != 1 else ''}, "
    f"{deleted_count} deletion{'s' if deleted_count != 1 else ''}, "
    f"{num_equal} match{'es' if num_equal != 1 else ''} (lines)\n"
    f"\nDiff map (line:char scale is 1:1 for single chars, 1:1 for char seqs):\n"
    f"  {diff_map}\n"
)

# Compute the len attribute: count the number of lines in the summary string
# R's len attribute counts meaningful lines in the formatted output
lines_in_summary = summary_str.split('\n')
# The len attribute is the number of non-empty segments or total lines
# From probing: len is 7, which is the number of lines when splitting by \n
# "\n" split gives: ['', 'Found...', '  0 insertions...', '', 'Diff map...', '  ....D...', '']
# That's 7 elements
len_attr = len(lines_in_summary)

# Print in R's format for as.character output
# R prints: [1] "<escaped string>"
# followed by attr(,"len")
# [1] 7

# Escape the string for R-style printing
escaped = summary_str.replace('\\', '\\\\').replace('"', '\\"')
escaped = escaped.replace('\n', '\\n')

print(f'[1] "{escaped}"')
print(f'attr(,"len")')
print(f'[1] {len_attr}')