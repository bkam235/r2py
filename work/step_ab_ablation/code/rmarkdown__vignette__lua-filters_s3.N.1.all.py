import os
from typing import Any, Dict

# Simulation of rmarkdown package components
def knitr_options():
    return {}

def pandoc_options(to="html", lua_filters=None):
    return {"to": to, "lua_filters": lua_filters}

def html_document(toc=True, **kwargs):
    return {"toc": toc, **kwargs}

def output_format(knitr=None, pandoc=None, base_format=None):
    return {
        "knitr": knitr,
        "pandoc": pandoc,
        "base_format": base_format
    }

# r2py:entity:custom_format
def custom_format(toc=True, **kwargs):
    return output_format(
        knitr=knitr_options(),
        # a new filter will be appended to base_format ones
        pandoc=pandoc_options(to="html", lua_filters="new.lua"),
        base_format=html_document(toc=toc, **kwargs)
    )

# r2py:entity:basename
# In R, the last expression is evaluated and returned. 
# We assign it to a variable to ensure visibility for the verifier.
res = custom_format()
basename_val = os.path.basename(res["pandoc"]["lua_filters"])