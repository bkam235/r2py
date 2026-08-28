# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.mlm.Rd
# Translated from R to Python

import pandas as pd
from scipy import stats
from statsmodels.formula.api import ols
import numpy as np

# Load mtcars data (built-in R dataset)
mtcars = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/mtcars.csv')

# Fit multiple regression model: mpg and disp predicted by wt
model = ols('Q("mpg") + Q("disp") ~ wt', data=mtcars).fit()

# Summarize model fit with tidiers
print(model.summary())
print("\nCoefficients with confidence intervals:")
print(model.conf_int())
