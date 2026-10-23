# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 3

import pandas as pd
from IPython.display import display, Markdown

# r2py:entity:knit_print.data.frame
def knit_print_data_frame(x, *args, **kwargs):
    # Approximating the knitr::kable behavior by converting the DataFrame to a Markdown table
    # and wrapping it in a format that mimics the R asis_output/knit_print behavior
    markdown_table = x.to_markdown()
    res = f"\n\n{markdown_table}"
    display(Markdown(res))

# r2py:entity:registerS3method
# In Python, we can't register S3 methods, but we can override the 
# default display behavior for pandas DataFrames in a notebook environment
# or use a custom display function.
pd.options.display.max_columns = None
pd.options.display.max_rows = None

# To simulate the effect of the R code provided, 
# we would call knit_print_data_frame(d) instead of print(d)