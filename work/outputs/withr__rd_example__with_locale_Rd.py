# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 11

import pandas as pd
import numpy as np
import locale
from plotnine import ggplot, aes, geom_point

# Note: Python's locale module is process-wide and depends on system-installed locales.
# Unlike R's withr, Python does not have a built-in context manager for temporary locale changes.
# This code assumes the locales 'es_ES', 'en_GB', 'it_IT', 'fr_FR', and 'en_US' are installed on the OS.

# r2py:entity:with_locale
def set_locale(loc_str):
    try:
        locale.setlocale(locale.LC_ALL, loc_str)
    except locale.Error:
        print(f"Locale {loc_str} not supported on this system.")

# 1. Plotting with date
# r2py:entity:df
df = pd.DataFrame({
    'date': pd.to_datetime(["2019-01-01", "2019-02-01"]),
    'value': [1, 2]
})
set_locale('es_ES')
print(ggplot(df, aes(x='date', y='value')) + geom_point())

# 2. Date formatting
import datetime

dates = [datetime.date(2000, m, 1) for m in range(1, 13)]

# r2py:entity:with_locale_1
set_locale('en_GB')
print([d.strftime('%B') for d in dates])

# r2py:entity:with_locale_2
set_locale('es_ES')
print([d.strftime('%B') for d in dates])

# 3. Monetary/Locale conventions
# r2py:entity:with_locale_3
set_locale('it_IT')
print(locale.localeconv())

# r2py:entity:with_locale_4
set_locale('en_US')
print(locale.localeconv())

# 4. Sorting/Collation
# r2py:entity:x
x = ["bernard", "bÃ©rÃ©nice", "bÃ©atrice", "boris"]

# r2py:entity:with_locale_5
set_locale('fr_FR')
print(sorted(x))

# r2py:entity:with_locale_6
set_locale('C')
print(sorted(x))