# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 3

import string
from difflib import ndiff

# r2py:entity:as.character
def diff_chr(target, current, format="raw", pager="off"):
    """
    Python equivalent of diffChr. 
    In R, letters is a vector. We treat lists of strings similarly.
    """
    # ndiff produces a delta of sequences
    result = list(ndiff(target, current))
    return result

# r2py:entity:as.character
def summary_diff(diff_obj):
    """
    Python equivalent of summary() for a Diff object.
    Typically summarizes the changes (additions, deletions).
    """
    added = sum(1 for line in diff_obj if line.startswith('+ '))
    removed = sum(1 for line in diff_obj if line.startswith('- '))
    return f"Diff summary: {removed} removals, {added} additions"

# letters in R: "a", "b", ..., "z"
letters = list(string.ascii_lowercase)

# letters[-c(5, 15)] removes 5th ('e') and 15th ('o') elements
# R is 1-indexed, Python is 0-indexed. 5th is index 4, 15th is index 14.
indices_to_remove = {4, 14}
letters_subset = [val for i, val in enumerate(letters) if i not in indices_to_remove]

# Execution
# r2py:entity:as.character
diff_result = diff_chr(letters, letters_subset, format="raw", pager="off")
summ = summary_diff(diff_result)
result_as_char = str(summ)

print(result_as_char)