# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 19

import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_line, facet_wrap
import random

# set.seed(1071)
# r2py:entity:set.seed
np.random.seed(1071)
random.seed(1071)

# Z.index <- as.Date(sample(12450:12500, 10))
# Note: R's Date origin is 1970-01-01. 12450 is approx 34 years later.
# r2py:entity:Z.index
dates_raw = np.random.choice(np.arange(12450, 12501), 10, replace=False)
Z_index = pd.to_datetime(dates_raw, unit='D', origin='1970-01-01')

# Z.data <- matrix(rnorm(30), ncol = 3)
# colnames(Z.data) <- c("Aa", "Bb", "Cc")
# r2py:entity:Z.data
Z_data = np.random.randn(10, 3)
# r2py:entity:colnames(Z.data)
columns = ["Aa", "Bb", "Cc"]

# Z <- zoo(Z.data, Z.index)
# r2py:entity:Z
Z = pd.DataFrame(Z_data, index=Z_index, columns=columns)

# tidy(Z)
# broom::tidy for zoo converts wide data to long format
# r2py:entity:tidy
tidy_Z = Z.reset_index().melt(id_vars='index', var_name='series', value_name='value')
print(tidy_Z)

# ggplot(tidy(Z), aes(index, value, color = series)) + geom_line()
# r2py:entity:ggplot
p1 = (ggplot(tidy_Z, aes('index', 'value', color='series')) 
# r2py:entity:geom_line
     + geom_line())
print(p1)

# ggplot(tidy(Z), aes(index, value)) + geom_line() + facet_wrap(~series, ncol = 1)
# r2py:entity:ggplot_1
p2 = (ggplot(tidy_Z, aes('index', 'value')) 
# r2py:entity:geom_line_1
     + geom_line() 
# r2py:entity:facet_wrap
     + facet_wrap('series', ncol=1))
print(p2)

# Zrolled <- rollmean(Z, 5)
# r2py:entity:Zrolled
Zrolled = Z.rolling(window=5).mean()

# ggplot(tidy(Zrolled), aes(index, value, color = series)) + geom_line()
# r2py:entity:ggplot_2
tidy_Zrolled = Zrolled.reset_index().melt(id_vars='index', var_name='series', value_name='value')
p3 = (ggplot(tidy_Zrolled, aes('index', 'value', color='series')) 
# r2py:entity:geom_line_2
     + geom_line())
print(p3)