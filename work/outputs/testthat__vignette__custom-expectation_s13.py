import pytest

# r2py:entity:expect_s3_class
def expect_s3_class(object, class_val, exact=False):
    # Mimic the logic of R's expect_s3_class
    # check_bool(exact)
    if not isinstance(exact, bool):
        raise TypeError("exact must be a boolean")
    
    if class_val is None: # Handling NA equivalent
        # S3 objects in Python aren't native, but we check if it's a custom object
        if hasattr(object, '__class__'):
            pytest.fail("Expected object not to be an S3 object.")
    elif isinstance(class_val, str):
        # Simplified S3 class check: in Python, this is usually checking __class__.__name__ or isinstance
        if not hasattr(object, '__class__'):
            pytest.fail("Expected object to be an S3 object.")
        
        obj_class = object.__class__.__name__
        if exact and obj_class != class_val:
            pytest.fail(f"Expected object to have class {class_val}. Actual class: {obj_class}")
        elif not isinstance(object, type(class_val)) and obj_class != class_val:
            # Simplified inherits check
            pytest.fail(f"Expected object to inherit from {class_val}. Actual class: {obj_class}")
    else:
        # R's stop_input_type is called when class is not character or NA
        # This is where the R source fails because 1 is passed as class
        raise TypeError(f"class must be a character vector or NA, not {type(class_val).__name__}")

# R: suppressPackageStartupMessages(library(testthat))
# Equivalent to importing the testing framework quietly

# R: try({ expect_s3_class(x1, 1) })
# r2py:entity:expect_s3_class
try:
    # x1 is undefined in the R snippet, causing NameError in Python
    # But the R function would have failed on the class argument '1' regardless.
    expect_s3_class(x1, 1)
except Exception:
    # R's try() suppresses the error output by default in this context
    pass