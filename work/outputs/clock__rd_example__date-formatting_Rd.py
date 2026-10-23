# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 7

import pandas as pd
from datetime import datetime
import locale

# x <- as.Date("2019-01-01")
# r2py:entity:x
x = pd.to_datetime("2019-01-01")

# date_format(x)
# r2py:entity:date_format
print(x.strftime('%Y-%m-%d'))

# date_format(x, format = "year: %Y, month: %m, day: %d")
# r2py:entity:date_format_1
print(x.strftime("year: %Y, month: %m, day: %d"))

# date_format(x, format = "%A, %B %d, %Y")
# r2py:entity:date_format_2
print(x.strftime("%A, %B %d, %Y"))

# date_format(x, format = "%A, %B %d, %Y", locale = clock_locale("fr"))
# r2py:entity:date_format_3
try:
    locale.setlocale(locale.LC_TIME, "fr_FR.UTF-8")
    print(x.strftime("%A, %B %d, %Y"))
except locale.Error:
    print("French locale not installed on this system")