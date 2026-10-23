# Translated from <R script> by r2py v0.3.0
# Model: claude-sonnet-4-6  ScriptMap entities: 3

import difflib

# r2py:entity:as.character
letters = list('abcdefghijklmnopqrstuvwxyz')
current = [c for i, c in enumerate(letters) if i + 1 not in (5, 15)]

# Compute diff using difflib
opcodes = difflib.SequenceMatcher(None, letters, current).get_opcodes()

insertions = 0
deletions = 0
matches = 0
for tag, i1, i2, j1, j2 in opcodes:
    if tag == 'equal':
        matches += (i2 - i1)
    elif tag == 'insert':
        insertions += (j2 - j1)
    elif tag == 'delete':
        deletions += (i2 - i1)
    elif tag == 'replace':
        deletions += (i2 - i1)
        insertions += (j2 - j1)

# Count hunks (non-equal blocks)
hunks = sum(1 for tag, *_ in opcodes if tag != 'equal')

# Build diff map - '.' for match, 'D' for deletion, 'I' for insertion
diff_map = []
for tag, i1, i2, j1, j2 in opcodes:
    if tag == 'equal':
        diff_map.extend(['.'] * (i2 - i1))
    elif tag == 'delete':
        diff_map.extend(['D'] * (i2 - i1))
    elif tag == 'insert':
        diff_map.extend(['I'] * (j2 - j1))
    elif tag == 'replace':
        diff_map.extend(['D'] * (i2 - i1))
        diff_map.extend(['I'] * (j2 - j1))

diff_map_str = ''.join(diff_map)

result = f"\nFound differences in {hunks} hunks:\n  {insertions} insertions, {deletions} deletions, {matches} matches (lines)\n\nDiff map (line:char scale is 1:1 for single chars, 1:1 for char seqs):\n  {diff_map_str}\n"

# as.character returns a character vector with length attribute
print(f'[1] {repr(result)}')
print('attr(,"len")')
print(f'[1] {len(result.split(chr(10))) - 1}')  # count newlines for len