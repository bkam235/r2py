# r2py crawler metadata
# package: diffobj
# source_type: rd_example
# topic: as.character-DiffSummary-method.Rd
# Translated from R to Python

import difflib

# Create two lists of strings (simulating R's letters vector)
letters = [chr(97 + i) for i in range(26)]  # a-z
letters_modified = letters[:4] + letters[5:14] + letters[15:]  # Remove 'e' and 'o'

# Create a diff summary
differ = difflib.Differ()
diff_result = list(differ.compare(letters, letters_modified))

# Print the diff as character representation
for line in diff_result:
    print(line)

# Alternative: get unified diff format
print("\n--- Unified diff format ---")
unified_diff = difflib.unified_diff(letters, letters_modified, lineterm='')
for line in unified_diff:
    print(line)
