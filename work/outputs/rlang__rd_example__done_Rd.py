import pandas as pd
import numpy as np

# Simulate rlang's boxing mechanism
# r2py:entity:x
class RLangBox:
    def __init__(self, value, class_name=None, empty=False):
        self.value = value
        self.class_name = class_name
        self.empty = empty
        self.data = [value]

    def __repr__(self):
        # R's print method for rlang boxes of type 'done' 
        # prints '<done>' then the value on the next line.
        if self.class_name == "rlang_box_done":
            return f"<done>\n[1] {self.value}"
        return f"[{self.value}]"

def done(x):
    # R source: new_box(maybe_missing(x), class_val= "rlang_box_done", empty = missing(x))
    return RLangBox(x, class_name="rlang_box_done", empty=False)

# r2py:entity:is_done_box
def is_done_box(x, empty=None):
    # R source: if (!inherits(x, "rlang_box_done")) { return(FALSE) }
    if not hasattr(x, 'class_name') or x.class_name != "rlang_box_done":
        return False
    # R source: if (is_null(empty)) { return(TRUE) }
    if empty is None:
        return True
    # R source: attr(x, "empty") == empty
    return x.empty == empty

# Translation of the logic
# suppressPackageStartupMessages(library(rlang))

# done(3)
# r2py:entity:done
res_done = done(3)
print(res_done)

# x <- done(3)
# r2py:entity:x
x = done(3)

# is_done_box(x)
# r2py:entity:is_done_box
res_is_done = is_done_box(x)
# R's print for a single logical is [1] TRUE
print(f"[1] {res_is_done}")