# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import numpy as np

# r2py:entity:rep
def as_bit(x):
    """
    Convert input to a bit array.
    In Python, we use a boolean numpy array as the equivalent of the 'bit' class.
    """
    return np.array(x, dtype=bool)

# r2py:entity:rep_2
def as_bitwhich(x):
    """
    Convert a logical/bit vector to a bit vector representing the 
    positions of TRUE values.
    In the context of the R 'bit' package, as.bitwhich on a logical vector
    essentially returns a bit vector of the same values if it's already 
    logical/bit.
    """
    x_arr = np.array(x, dtype=bool)
    return as_bit(x_arr)

# r2py:entity:rep
def rep(x, times=None, length_out=None):
    """
    Equivalent to R's rep function for bit vectors.
    """
    if length_out is not None:
        # R's rep with length.out tiles the vector and then truncates/pads
        res = np.tile(x, int(np.ceil(length_out / len(x))))[:length_out]
        return res
    if times is not None:
        # R's rep(x, n) repeats the entire vector n times
        res = np.tile(x, times)
        return res
    return x

def r_print_bit(x, is_bitwhich=False):
    """
    Custom print formatter to match R's bit/bitwhich output.
    """
    length = len(x)
    # R's bit objects print memory info. We simulate the header.
    #- bit: "bit length=X occupying only Y int32"
    #- bitwhich: "bitwhich: P/ X occupying only Y int32 in Z representation"
    if is_bitwhich:
        pos_count = np.sum(x)
        # Simulation of the "occupying only... representation" string
        print(f"bitwhich: {pos_count}/ {length} occupying only  {max(1, (length+31)//32)} int32 in {'FALSE' if pos_count == 0 else '1'} representation")
    else:
        print(f"bit length={length} occupying only {max(1, (length+31)//32)} int32")
    
    # Print 1-based indices
    indices = " ".join(map(str, range(1, length + 1)))
    print(indices)
    
    # Print FALSE/TRUE values
    vals = " ".join(["TRUE" if val else "FALSE" for val in x])
    print(vals)

# rep(as.bit(c(FALSE, TRUE)), 2)
# r2py:entity:rep
res1 = rep(as_bit([False, True]), times=2)
r_print_bit(res1)

# rep(as.bit(c(FALSE, TRUE)), length.out=7)
# r2py:entity:rep_1
res2 = rep(as_bit([False, True]), length_out=7)
r_print_bit(res2)

# rep(as.bitwhich(c(FALSE, TRUE)), 2)
# r2py:entity:rep_2
res3 = rep(as_bitwhich([False, True]), times=2)
r_print_bit(res3, is_bitwhich=True)

# rep(as.bitwhich(c(FALSE, TRUE)), length.out=1)
# r2py:entity:rep_3
res4 = rep(as_bitwhich([False, True]), length_out=1)
r_print_bit(res4, is_bitwhich=True)