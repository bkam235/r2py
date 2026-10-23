import os
from typing import Any, Dict

# Since rmarkdown and its specific output_format/knitr/pandoc structures 
# are unique to the R ecosystem, we simulate the object structure 
# using dictionaries and classes to maintain the logic.

# r2py:entity:custom_format
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

def custom_format(toc=True, **kwargs):
    # This simulates rmarkdown::output_format
    return {
        "knitr": knitr_options(),
        "pandoc": pandoc_options(to="html", lua_filters="new.lua"),
        "base_format": html_document(toc=toc, **kwargs)
    }

# Execution
# r2py:entity:basename
res = custom_format()
# basename() in R is equivalent to os.path.basename() in Python
# We assign to a variable to match R's evaluation of the expression
basename_res = os.path.basename(res["pandoc"].lua_filters)
print(basename_res)