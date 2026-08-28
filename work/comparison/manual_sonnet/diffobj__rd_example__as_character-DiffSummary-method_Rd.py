# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: as.character-DiffSummary-method.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diffobj\help
# lines: 4

import difflib

# R's `letters` is a-z; letters[-c(5, 15)] removes 1-indexed positions 5 ("e") and 15 ("o")
letters = list("abcdefghijklmnopqrstuvwxyz")
letters_modified = [c for i, c in enumerate(letters, start=1) if i not in (5, 15)]

# Compute and print a unified diff summary (equivalent to as.character(summary(diffChr(...))))
diff = list(difflib.unified_diff(letters, letters_modified, lineterm=""))
print("\n".join(diff))
