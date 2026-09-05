# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:entity:bp_...elt
def dot_elt(n, *args):
    """
    Mimics the functionality of backports::...elt,
    which typically returns the n-th element of the dots.
    """
    if n < 1 or n > len(args):
        raise IndexError("Element index out of range")
    return args[n - 1]

# r2py:entity:foo
def foo(n, *args):
    return dot_elt(n, *args)

# r2py:entity:foo_1
print(foo(2, "a", "b", "c"))