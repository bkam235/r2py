# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import pandas as pd
import numpy as np

def writeLines(text, sep="\n"):
    if isinstance(text, list):
        print(sep.join(text))
    else:
        print(text, end="")

# Mocking proxy.pr_DB and summary(pr_DB, "long") logic
# Based on the proxy package, pr_DB contains registry of distance/similarity measures
# x = summary(pr_DB, "long") results in a data frame/list with distance, type, formula, names
# Since pr_DB is a registry, we simulate the structure returned by summary(pr_DB, "long")
# Note: In a real environment, this would come from the `proxy` library equivalent.
# Here we provide the structure required for the script to execute.

# Example data approximating proxy::summary(pr_DB, "long")
# r2py:entity:x
x_data = {
    'distance': [False, False, True, True],
    'type': ['similarity', 'similarity', 'distance', 'distance'],
    'formula': ['1 - d', '1 / (1 + d)', 'sqrt(sum((x-y)^2))', 'sum(abs(x-y))'],
    'names': [['cosine', 'cos'], ['pearson', 'cor'], ['euclidean'], ['manhattan']]
}
x = pd.DataFrame(x_data)

# R: FUN <- function(index) { ... }
# r2py:entity:FUN
def FUN(index):
    # R's which(index) returns 1-based indices where condition is True
    # Python equivalent: np.where(index)[0] returns 0-based indices
    indices = np.where(index)[0]
    for i in indices:
        # R: paste(x$names[[i]], collapse = ", ")
        names_list = x['names'].iloc[i]
        names_str = ", ".join(names_list)
        writeLines(f"Aliases: {names_str}")
        
        # R: x$type[i]
        writeLines(f"Type   : {x['type'].iloc[i]}")
        
        # R: x$formula[i]
        writeLines(f"Formula: {x['formula'].iloc[i]}\n")

# code chunk number 2: FUN(x$distance == FALSE)
# r2py:entity:FUN_1
FUN(x['distance'] == False)

# code chunk number 3: FUN(x$distance == TRUE)
# r2py:entity:FUN_2
FUN(x['distance'] == True)