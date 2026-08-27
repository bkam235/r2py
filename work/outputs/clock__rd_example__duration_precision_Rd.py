# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 5

import numpy as np
import pandas as pd

# r2py:entity:duration_precision
class ClockDuration:
    def __init__(self, values, precision):
        self.values = np.array(values)
        self.precision = precision

    def __repr__(self):
        return f"ClockDuration({self.values}, precision={self.precision})"

def precision_to_string(precision):
    mapping = {
        "PRECISION_NANOSECOND": "nanoseconds",
        "PRECISION_SECOND": "seconds",
        "PRECISION_QUARTER": "quarters"
    }
    return mapping.get(precision, str(precision))

def duration_precision(x):
    if isinstance(x, ClockDuration):
        return precision_to_string(x.precision)
    elif isinstance(x, list) or isinstance(x, np.ndarray):
        # If it's a collection of ClockDurations
        return [precision_to_string(item.precision) for item in x]
    else:
        raise TypeError(f"x must be a <clock_duration>, not {type(x)}")

def duration_helper(n, precision):
    # Convert input to array to support both single integers and sequences (like 1:5)
    n_val = np.array(n)
    if n_val.ndim == 0:
        return ClockDuration(n_val.item(), precision)
    else:
        # In R, duration_quarters(1:5) returns a vector of durations
        return [ClockDuration(val, precision) for val in n_val]

def duration_seconds(n=0):
    return duration_helper(n, "PRECISION_SECOND")

def duration_nanoseconds(n=0):
    return duration_helper(n, "PRECISION_NANOSECOND")

def duration_quarters(n=0):
    return duration_helper(n, "PRECISION_QUARTER")

# Execution
# r2py:entity:duration_precision
print(duration_precision(duration_seconds(1)))
# r2py:entity:duration_precision_1
print(duration_precision(duration_nanoseconds(2)))
# r2py:entity:duration_precision_2
print(duration_precision(duration_quarters(np.arange(1, 6))))