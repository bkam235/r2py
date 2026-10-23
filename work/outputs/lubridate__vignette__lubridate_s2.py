# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 4

import pandas as pd

# r2py:entity:ymd
def ymd(x, quiet=False, tz=None, locale=None, truncated=0):
    res = pd.to_datetime(x, format='%Y%m%d')
    return res.strftime('%Y-%m-%d')

# r2py:entity:mdy
def mdy(x, quiet=False, tz=None, locale=None, truncated=0):
    res = pd.to_datetime(x, format='%m-%d-%Y')
    return res.strftime('%Y-%m-%d')

# r2py:entity:dmy
def dmy(x, quiet=False, tz=None, locale=None, truncated=0):
    res = pd.to_datetime(x, format='%d/%m/%Y')
    return res.strftime('%Y-%m-%d')

# r2py:entity:ymd
print(f'[1] "{ymd("20110604")}"')
# r2py:entity:mdy
print(f'[1] "{mdy("06-04-2011")}"')
# r2py:entity:dmy
print(f'[1] "{dmy("04/06/2011")}"')