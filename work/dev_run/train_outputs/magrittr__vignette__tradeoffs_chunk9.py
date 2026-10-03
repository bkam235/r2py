# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import random
import pprint

# suppressPackageStartupMessages(library(magrittr))
pass

def r_print_list(lst):
    """Helper to simulate R's list printing format."""
    for i, item in enumerate(lst, 1):
        print(f"[[{i}]]")
        print(f" [1] {'  '.join(map(str, item))}")
        print("")

# sample(10) %>% list(., .)
# r2py:entity:sample
sample_val = random.sample(range(1, 11), 10)
# r2py:entity:list
res1_list = [sample_val, sample_val]
r_print_list(res1_list)

# list(sample(10), sample(10))
# r2py:entity:list_1
res2_list = [random.sample(range(1, 11), 10), random.sample(range(1, 11), 10)]
r_print_list(res2_list)