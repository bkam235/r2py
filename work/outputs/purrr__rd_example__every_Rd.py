# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 9

import numpy as np

# r2py:entity:every
def every(x, p):
    """Check if all elements in x satisfy predicate p."""
    return all(p(i) for i in x)

# r2py:entity:some
def some(x, p):
    """Check if any element in x satisfies predicate p."""
    return any(p(i) for i in x)

# r2py:entity:none
def none(x, p):
    """Check if no elements in x satisfy predicate p."""
    return not any(p(i) for i in x)

def is_numeric(x):
    """R's is.numeric checks for numeric/double types."""
    return isinstance(x, (int, float, np.number))

def is_integer(x):
    """R's is.integer checks for integer types."""
    return isinstance(x, (int, np.integer))

def is_character(x):
    """R's is.character checks for string types."""
    return isinstance(x, str)

# r2py:entity:some_2
def is_true(x):
    """R's rlang::is_true checks if value is exactly TRUE (not NA)."""
    return x is True

# Equivalent to: x <- list(0:10, 5.5)
# In R, 0:10 is an integer vector, 5.5 is a double.
# We use lists to mimic the R list structure.
# r2py:entity:x
x = [list(range(11)), 5.5]

# r2py:entity:every
print(every(x, lambda item: all(is_numeric(v) if isinstance(item, list) else is_numeric(item) for v in (item if isinstance(item, list) else [item]))))
# The R script uses is.numeric on the list elements. 
# Since x is a list containing a vector and a double, every(is.numeric) checks if each element is numeric.
# Note: In R, is.numeric(0:10) is TRUE. In Python, we check if the elements of the list satisfy the condition.
# To match R's behavior on lists of vectors:
print(every(x, lambda i: is_numeric(i) if not isinstance(i, list) else all(is_numeric(v) for v in i)))
# r2py:entity:every_1
print(every(x, lambda i: is_integer(i) if not isinstance(i, list) else all(is_integer(v) for v in i)))
# r2py:entity:some
print(some(x, lambda i: is_integer(i) if not isinstance(i, list) else all(is_integer(v) for v in i)))
# r2py:entity:none
print(none(x, lambda i: is_character(i) if not isinstance(i, list) else all(is_character(v) for v in i)))

# Missing values are propagated:
# In R, some(list(NA, FALSE), identity) returns NA
# Python's any() on [None, False] would be False, but R's NA propagates.
# r2py:entity:some_1
def some_with_na(x, p):
    results = [p(i) for i in x]
    if any(v is None for v in results):
        return None
    return any(results)

print(some_with_na([None, False], lambda x: x))

# If you need to use these functions in a context where missing values
# are unsafe, make sure to use safe predicates:
# rlang::is_true handles NA by returning FALSE
# r2py:entity:some_2
res = "foo" if some_with_na([None, False], is_true) else "bar"
print(res)