# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import numpy as np
import time
from functools import wraps

# Mimicking purrr::slowly by creating a wrapper that adds a delay
# r2py:entity:slow_runif
def slowly(func, rate):
    @wraps(func)
    def wrapper(*args, **kwargs):
        time.sleep(rate)
        return func(*args, **kwargs)
    return wrapper

# rate <- rate_delay(0.1)
# r2py:entity:rate
rate = 0.1

# slow_runif <- slowly(\(x) runif(1), rate = rate, quiet = FALSE)
slow_runif = slowly(lambda x: np.random.uniform(0, 1), rate=rate)

# out <- map(1:5, slow_runif)
# r2py:entity:out
out = [slow_runif(x) for x in range(1, 6)]