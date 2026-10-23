# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

# r2py:entity:f
def f(x, **kwargs, foofy=8):
    if kwargs:
        raise TypeError("Unexpected keyword arguments found")
    return x + foofy

# r2py:entity:try
try:
    f(1, foof=4)
except Exception as e:
    print(f"Error: {e}")

# r2py:entity:f_1
print(f(1, foofy=4))