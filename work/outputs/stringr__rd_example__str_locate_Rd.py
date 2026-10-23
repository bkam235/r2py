# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 11

import pandas as pd
import re

# r2py:entity:fruit
fruit = ["apple", "banana", "pear", "pineapple"]

# r2py:entity:str_locate
def str_locate(text_list, pattern):
    results = []
    for text in text_list:
        match = re.search(pattern, text)
        if match:
            # R's str_locate is 1-indexed
            results.append([match.start() + 1, match.end()])
        else:
            results.append([np.nan, np.nan])
    return pd.DataFrame(results, columns=["start", "end"])

# r2py:entity:str_locate_all
def str_locate_all(text_list, pattern):
    results = []
    for text in text_list:
        matches = [(m.start() + 1, m.end()) for m in re.finditer(f'(?={pattern})' if pattern == "" else pattern, text)]
        results.append(matches)
    return results

import numpy as np

# str_locate(fruit, "$")
# r2py:entity:str_locate
print(str_locate(fruit, "$"))

# str_locate(fruit, "a")
# r2py:entity:str_locate_1
print(str_locate(fruit, "a"))

# str_locate(fruit, "e")
# r2py:entity:str_locate_2
print(str_locate(fruit, "e"))

# str_locate(fruit, c("a", "b", "p", "p")) -> interpreted as regex OR
# r2py:entity:str_locate_3
print(str_locate(fruit, "|".join(["a", "b", "p", "p"])))

# str_locate_all(fruit, "a")
# r2py:entity:str_locate_all
print(str_locate_all(fruit, "a"))

# str_locate_all(fruit, "e")
# r2py:entity:str_locate_all_1
print(str_locate_all(fruit, "e"))

# str_locate_all(fruit, c("a", "b", "p", "p"))
# r2py:entity:str_locate_all_2
print(str_locate_all(fruit, "|".join(["a", "b", "p", "p"])))

# str_locate_all(fruit, "")
# r2py:entity:str_locate_all_3
print(str_locate_all(fruit, ""))