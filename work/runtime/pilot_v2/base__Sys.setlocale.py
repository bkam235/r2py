import locale as py_locale
import numpy as np

def r_Sys_setlocale(category="LC_ALL", locale=""):
    # R's valid categories
    lc_categories = ["LC_CTYPE", "LC_COLLATE", "LC_TIME", "LC_NUMERIC", "LC_MONETARY", "LC_MESSAGES", "LC_ALL"]
    
    # Handle category input (handles cases like rep("LC_TIME", 1))
    cat_val = category
    if isinstance(category, np.ndarray):
        cat_val = category[0]
    elif isinstance(category, list):
        cat_val = category[0]
        
    if cat_val not in lc_categories:
        raise ValueError("invalid 'category' argument")

    # Mapping R categories to Python's locale constants.
    mapping = {
        "LC_CTYPE": getattr(py_locale, "LC_CTYPE", None),
        "LC_COLLATE": getattr(py_locale, "LC_COLLATE", None),
        "LC_TIME": getattr(py_locale, "LC_TIME", None),
        "LC_NUMERIC": getattr(py_locale, "LC_NUMERIC", None),
        "LC_MONETARY": getattr(py_locale, "LC_MONETARY", None),
        "LC_MESSAGES": getattr(py_locale, "LC_MESSAGES", None),
        "LC_ALL": getattr(py_locale, "LC_ALL", None),
    }
    
    py_cat = mapping[cat_val]
    
    if py_cat is not None:
        py_loc = locale if locale != "" else None
        try:
            # Attempt to set the locale
            py_locale.setlocale(py_cat, py_loc)
            # Return the result of the set operation
            current_locale = py_locale.setlocale(py_cat)
        except (py_locale.Error, ValueError):
            # In R, if an invalid locale is passed to Sys.setlocale, 
            # it often returns an empty string "" or the current locale depending on the OS.
            # The failing case shows R returning "" when letters[1] (invalid locale) is passed.
            current_locale = ""
    else:
        current_locale = locale if locale != "" else "C"

    # R returns a character vector. 
    # Given the examples: [1] "en_US.UTF-8", return as a list of str.
    # To match the failing case where R returns "", we ensure we return [current_locale].
    return [current_locale]
