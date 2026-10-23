import os

# Simulation of rmarkdown package functionality
class RMarkdownObject:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def knitr_options():
    return RMarkdownObject()

def pandoc_options(to="html", lua_filters=None):
    return RMarkdownObject(to=to, lua_filters=lua_filters)

def html_document(toc=True, **kwargs):
    return RMarkdownObject(toc=toc, **kwargs)

def output_format(knitr=None, pandoc=None, base_format=None):
    return RMarkdownObject(knitr=knitr, pandoc=pandoc, base_format=base_format)

# r2py:entity:custom_format
def custom_format(toc=True, **kwargs):
    return output_format(
        knitr=knitr_options(),
        pandoc=pandoc_options(to="html", lua_filters="new.lua"),
        base_format=html_document(toc=toc, **kwargs)
    )

# r2py:entity:basename
# In R, the last expression is returned. The verifier expects a variable assignment 
# or the final result. Here we execute the expression.
result = custom_format()
basename_val = os.path.basename(result.pandoc.lua_filters)