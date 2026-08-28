# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: as.character-DiffSummary-method.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 4

import difflib
import string

letters = list(string.ascii_lowercase)
letters_modified = [ch for ch in letters if ch not in ("e", "o")]

diff = list(difflib.unified_diff(letters, letters_modified, lineterm=""))
print("\n".join(diff))
