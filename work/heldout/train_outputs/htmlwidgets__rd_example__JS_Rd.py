# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd
import numpy as np

# r2py:entity:JS
class JSEval(str):
    def __repr__(self):
        # Mimic R output: [1] "string" \n attr(,"class") \n [1] "JS_EVAL"
        # For multiline strings, R's print.default handles \n as literal characters in the quotes
        escaped_val = self.replace('\n', '\\n')
        return f'[1] "{escaped_val}"\nattr(,"class")\n[1] "JS_EVAL"'

def JS(*args):
    """
    Python implementation of htmlwidgets::JS.
    Collapses character arguments with newlines and marks them as JS_EVAL.
    """
    if not args:
        return None
    # Ensure all arguments are strings
    for arg in args:
        if not isinstance(arg, str):
            raise TypeError("The arguments for JS() must be a character vector")
    
    # paste(x, collapse = "\n")
    result = "\n".join(args)
    
    return JSEval(result)

# library(htmlwidgets)
# (Functionality provided by the JS helper above)

# JS('1 + 1')
# r2py:entity:JS
JS_result = JS('1 + 1')
print(repr(JS_result))

# list(x = JS('function(foo) {return foo;}'), y = 1:10)
# r2py:entity:list
list_result = {
    "x": JS('function(foo) {return foo;}'),
    "y": np.arange(1, 11)
}
# Mimicking R list print: $x \n [1] "..." \n attr(,"class") \n [1] "JS_EVAL" \n $y \n [1] 1 2 ...
print(f"$x\n{repr(list_result['x'])}\n\n$y\n { ' '.join(map(str, list_result['y'])) }")

# JS('function(x) {', 'return x + 1;', '}')
# r2py:entity:JS_1
JS_result_1 = JS('function(x) {', 'return x + 1;', '}')
print(repr(JS_result_1))