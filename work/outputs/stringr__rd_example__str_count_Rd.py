# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 9

import pandas as pd
import re

# r2py:entity:fruit
fruit = ["apple", "banana", "pear", "pineapple"]

# str_count(fruit, "a")
# r2py:entity:str_count
print([s.count("a") for s in fruit])

# str_count(fruit, "p")
# r2py:entity:str_count_1
print([s.count("p") for s in fruit])

# str_count(fruit, "e")
# r2py:entity:str_count_2
print([s.count("e") for s in fruit])

# str_count(fruit, c("a", "b", "p", "p"))
# R's str_count with a vector of patterns returns the count for the first match or combined; 
# however, typically in this context it behaves as an OR regex.
# r2py:entity:str_count_3
print([len(re.findall(r'[abp]', s)) for s in fruit])

# str_count(c("a.", "...", ".a.a"), ".")
# In R, "." is a regex wildcard.
# r2py:entity:str_count_4
texts = ["a.", "...", ".a.a"]
print([len(re.findall(r'.', s)) for s in texts])

# str_count(c("a.", "...", ".a.a"), fixed("."))
# fixed(".") treats the dot as a literal character.
# r2py:entity:str_count_5
print([s.count(".") for s in texts])