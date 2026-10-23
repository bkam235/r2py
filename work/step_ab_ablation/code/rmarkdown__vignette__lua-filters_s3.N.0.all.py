import os
from typing import Any, Dict

# r2py:entity:import_rmarkdown
# Simulation of rmarkdown package structures
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

def output_format(knitr=None, pandoc=None, base_format=None):
    return RMarkdownOptions(knitr=knitr, pandoc=pandoc, base_format=base_format)

# r2py:entity:custom_format
def custom_format(toc=True, **kwargs):
    return output_format(
        knitr=knitr_options(),
        pandoc=pandoc_options(to="html", lua_filters="new.lua"),
        base_format=html_document(toc=toc, **kwargs)
    )

# r2py:entity:basename
# R: basename(custom_format()$pandoc$lua_filters)
result_format = custom_format()
basename_val = os.path.basename(result_format.pandoc.lua_filters)