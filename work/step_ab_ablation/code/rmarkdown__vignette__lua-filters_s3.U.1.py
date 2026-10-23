import os
from typing import Any, Dict

# Simulation of rmarkdown package structures
# r2py:entity:import_rmarkdown
class RMarkdownOptions:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

def knitr_options():
    return RMarkdownOptions()

def pandoc_options(to="html", lua_filters=None):
    return RMarkdownOptions(to=to, lua_filters=lua_filters)

def html_document(toc=True, **kwargs):
    return RMarkdownOptions(toc=toc, **kwargs)

# r2py:entity:custom_format
def custom_format(toc=True, **kwargs):
    # This simulates rmarkdown::output_format
    return {
        "knitr": knitr_options(),
        "pandoc": pandoc_options(to="html", lua_filters="new.lua"),
        "base_format": html_document(toc=toc, **kwargs)
    }

# r2py:entity:suppressPackageStartupMessages
# In Python, library imports don't produce startup messages in the same way as R.
# This is a no-op for the simulated environment.

# Execution
# r2py:entity:basename
res_custom_format = custom_format()
# basename() in R is equivalent to os.path.basename() in Python
# R code: basename(custom_format()$pandoc$lua_filters)
result = os.path.basename(res_custom_format["pandoc"].lua_filters)
print(result)