import os

# Simulated rmarkdown functions to match R behavior
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
        pandoc=pandoc_options(to="html", lua_filters="new.lua"),
        base_format=html_document(toc=toc, **kwargs)
    )

# r2py:entity:basename
# In R, the last line is an expression that is implicitly printed.
# We assign the result to a variable to mimic R's behavior if needed, 
# but the specific call is:
result = custom_format()
# R: basename(custom_format()$pandoc$lua_filters)
basename_val = os.path.basename(result["pandoc"]["lua_filters"])