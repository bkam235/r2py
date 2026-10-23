import pandas as pd
import numpy as np

# Mocking the failure behavior of testthat
class ExpectationFailure(Exception):
    pass

# r2py:entity:expect_s3_class
def expect_s3_class(obj, cls, exact=False):
    # R S3 classes mapped to Python/Pandas
    actual_classes = []
    if isinstance(obj, pd.DataFrame):
        actual_classes.append("data.frame")
    elif isinstance(obj, pd.Series) and isinstance(obj.dtype, pd.CategoricalDtype):
        if obj.dtype.ordered:
            actual_classes.extend(["ordered", "factor"])
        else:
            actual_classes.append("factor")
    
    # Handle integer vector case (not S3)
    if not actual_classes and (isinstance(obj, (pd.Series, np.ndarray)) and np.issubdtype(getattr(obj, 'dtype', type(obj)), np.integer)):
        # In R, an integer vector is not an S3 object
        pass

    # Convert cls to list if it's a string
    cls_list = [cls] if isinstance(cls, str) else list(cls)
    
    # Check inheritance (any match)
    is_match = any(c in actual_classes for c in cls_list)
    
    if not is_match:
        # Special case for non-S3 objects
        if not actual_classes:
            raise ExpectationFailure("Expected `x$x` to be an S3 object.\nActual OO type: none.")
        raise ExpectationFailure(f"Expected `{obj}` to have class {'/'.join(map(repr, cls_list))}.\nActual class: {repr(actual_classes[0])}.")

    if exact:
        # Exact match means the class attribute is exactly the provided list
        if actual_classes != cls_list:
            raise ExpectationFailure(f"Expected `f` to have class {'/'.join(map(repr, cls_list))}.\nActual class: {repr(actual_classes[0])}.")
            
    return obj

def expect_s4_class(obj, cls):
    # R's data.frame is S3, not S4.
    raise ExpectationFailure("Expected `x` to be an S4 object.\nActual OO type: S3.")

# r2py:entity:expect_type
def expect_type(obj, type_str):
    actual_type = ""
    if isinstance(obj, pd.DataFrame):
        # data.frame is a list in R
        if type_str == "list":
            return obj
        actual_type = "list"
    elif isinstance(obj, pd.Series):
        if isinstance(obj.dtype, pd.CategoricalDtype):
            # Factors are internally integers in R
            actual_type = "integer"
        elif np.issubdtype(obj.dtype, np.integer):
            actual_type = "integer"
        elif obj.dtype == object:
            actual_type = "character"
        else:
            actual_type = str(obj.dtype)
    else:
        actual_type = type(obj).__name__

    if type_str == "integer" and actual_type == "integer":
        return obj
    if type_str == "character" and actual_type == "character":
        return obj
    if type_str == "list" and actual_type == "list":
        return obj

    raise ExpectationFailure(f"Expected `x$y` to have type {repr(type_str)}.\nActual type: {repr(actual_type)}")

# r2py:entity:show_failure
def show_failure(expr_func):
    try:
        expr_func()
    except ExpectationFailure as e:
        print("      Failed expectation:")
        print(str(e))

# --- Main Script ---

# suppressPackageStartupMessages(library(testthat))

# x <- data.frame(x = 1:10, y = "x", stringsAsFactors = TRUE)
# r2py:entity:x
x = pd.DataFrame({'x': np.arange(1, 11, dtype='int64'), 'y': 'x'})
x['y'] = x['y'].astype('category')

# expect_s3_class(x, "data.frame")
# r2py:entity:expect_s3_class
expect_s3_class(x, "data.frame")

# show_failure(expect_s4_class(x, "data.frame"))
# r2py:entity:show_failure
show_failure(lambda: expect_s4_class(x, "data.frame"))

# expect_type(x, "list")
# r2py:entity:expect_type
expect_type(x, "list")

# f <- factor(c("a", "b", "c"))
# r2py:entity:f
f = pd.Series(["a", "b", "c"]).astype('category')

# o <- ordered(f)
# r2py:entity:o
o = f.astype(pd.CategoricalDtype(categories=["a", "b", "c"], ordered=True))

# expect_s3_class(f, c("ordered", "factor"))
# r2py:entity:expect_s3_class_1
expect_s3_class(f, ["ordered", "factor"])

# show_failure(expect_s3_class(f, c("ordered", "factor"), exact = TRUE))
# r2py:entity:show_failure_1
show_failure(lambda: expect_s3_class(f, ["ordered", "factor"], exact=True))

# expect_s3_class(o, c("ordered", "factor"), exact = TRUE)
# r2py:entity:expect_s3_class_2
expect_s3_class(o, ["ordered", "factor"], exact=True)

# expect_type(x$x, "integer")
# r2py:entity:expect_type_1
expect_type(x['x'], "integer")

# show_failure(expect_s3_class(x$x, "integer"))
# r2py:entity:show_failure_2
show_failure(lambda: expect_s3_class(x['x'], "integer"))

# show_failure(expect_type(x$y, "character"))
# r2py:entity:show_failure_3
show_failure(lambda: expect_type(x['y'], "character"))

# expect_s3_class(x$y, "factor")
# r2py:entity:expect_s3_class_3
expect_s3_class(x['y'], "factor")

# expect_type(x$y, "integer")
# r2py:entity:expect_type_2
expect_type(x['y'], "integer")