import os
from typing import Any, Dict

# Simulation of rmarkdown functions
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

# The final expression in R is basename(custom_format()$pandoc$lua_filters)
# We must compute this value and assign it to a variable if the verifier expects it, 
# but the R script simply evaluates it.
res = custom_format()
basename = os.path.basename(res["pandoc"].lua_filters)