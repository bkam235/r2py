import os
from typing import Any, Dict

# Simulation of rmarkdown package functions
def knitr_options():
    return type('obj', (object,), {})()

def pandoc_options(to="html", lua_filters=None):
    return type('obj', (object,), {'to': to, 'lua_filters': lua_filters})()

def html_document(toc=True, **kwargs):
    return type('obj', (object,), {'toc': toc, **kwargs})()

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
        pandoc=pandoc_options(to="html", lua_filters="new.lua"),
        base_format=html_document(toc=toc, **kwargs)
    )

# Execution
# r2py:entity:basename
# The R expression is basename(custom_format()$pandoc$lua_filters)
# we need to capture this result.
res_val = custom_format()
basename_res = os.path.basename(res_val["pandoc"].lua_filters)