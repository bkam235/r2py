# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import numpy as np

# r2py:entity:sequence
def sequence(nvec, from_val=1, by=1, recycle=False):
    nvec = np.asarray(nvec, dtype=int)
    res = []
    for n in nvec:
        res.extend(range(from_val, from_val + n * by, by))
    return np.array(res)

# r2py:entity:vecseq
def vecseq(x, y=None, concat=True, eval_val=True):
    x = np.asarray(x, dtype=int)
    if y is None:
        y = x
        x = np.array([1], dtype=int)
    else:
        y = np.asarray(y, dtype=int)

    if concat:
        if eval_val:
            nx, ny = len(x), len(y)
            # Handle recycling logic equivalent to R's rep(..., length.out = ...)
            x_rep = np.tile(x, (ny // nx + 1)).astype(int)[:ny] if nx < ny else x
            y_rep = np.tile(y, (nx // ny + 1)).astype(int)[:nx] if ny < nx else y
            
            results = []
            for start, end in zip(x_rep, y_rep):
                if start <= end:
                    results.extend(range(start, end + 1))
                else:
                    results.extend(range(start, end - 1, -1))
            return np.array(results)
        else:
            # In R, this returns a language object (parsed expression). 
            # In Python, we represent this as a string expression.
            parts = [f"{x[i]}:{y[i]}" for i in range(len(x))]
            return f"c({', '.join(parts)})"
    else:
        if eval_val:
            results = []
            for start, end in zip(x, y):
                if start <= end:
                    results.append(list(range(start, end + 1)))
                else:
                    results.append(list(range(start, end - 1, -1)))
            return results
        else:
            # Returns a list of string expressions
            return [f"{x[i]}:{y[i]}" for i in range(len(x))]

# r2py:entity:sequence
print(sequence([3, 4]))
# r2py:entity:vecseq
print(vecseq([3, 4]))
# r2py:entity:vecseq_1
print(vecseq([1, 11], [5, 15]))
# r2py:entity:vecseq_2
print(vecseq([1, 11], [5, 15], concat=False, eval_val=False))
# r2py:entity:vecseq_3
print(vecseq([1, 11], [5, 15], concat=False, eval_val=True))
# r2py:entity:vecseq_4
print(vecseq([1, 11], [5, 15], concat=True, eval_val=False))
# r2py:entity:vecseq_5
print(vecseq([1, 11], [5, 15], concat=True, eval_val=True))