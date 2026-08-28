# Translated from <R script> by r2py v0.3.0
# Model: claude-haiku-4-5  ScriptMap entities: 3

import difflib

# r2py:entity:as.character
letters = [chr(i) for i in range(97, 123)]
letters_modified = letters[:4] + letters[5:14] + letters[15:]

differ = difflib.Differ()
diff_result = list(differ.compare(letters, letters_modified))

output = '\n'.join(diff_result)
print(output)