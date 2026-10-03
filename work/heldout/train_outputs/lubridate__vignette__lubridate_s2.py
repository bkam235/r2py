# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd

# r2py:entity:ymd
print(pd.to_datetime("20110604", format="%Y%m%d").strftime("%Y-%m-%d"))
# r2py:entity:mdy
print(pd.to_datetime("06-04-2011", format="%m-%d-%Y").strftime("%Y-%m-%d"))
# r2py:entity:dmy
print(pd.to_datetime("04/06/2011", format="%d/%m/%Y").strftime("%Y-%m-%d"))