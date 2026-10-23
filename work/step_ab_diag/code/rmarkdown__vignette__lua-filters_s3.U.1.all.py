# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

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
# In R: basename(custom_format()$pandoc$lua_filters)
res = custom_format()
basename_result = os.path.basename(res["pandoc"].lua_filters)