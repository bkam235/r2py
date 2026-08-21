# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

import numpy as np
# r2py:entity:handlers
from tqdm import tqdm

# r2py:entity:y
def slow_sum(data):
    total = 0
    # Using tqdm to emulate progressr's progress bar functionality
    for i in tqdm(data, desc="Calculating sum"):
        total += i
    return total

if __name__ == "__main__":
    y = slow_sum(np.arange(1, 11))
# r2py:entity:print
    print(y)