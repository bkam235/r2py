# r2py crawford metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_ecdf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 27

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, stat_ecdf

np.random.seed(1)

df = pd.DataFrame({
    "x": np.concatenate([np.random.normal(0, 3, 100), np.random.normal(0, 10, 100)]),
    "g": pd.Categorical(np.repeat([1, 2], 100)),
})

# Basic ECDF step plot
p1 = ggplot(df, aes("x")) + stat_ecdf(geom="step")
print(p1)

# ECDF without padding to +/- infinity
p2 = ggplot(df, aes("x")) + stat_ecdf(geom="step", pad=False)
print(p2)

# Multiple ECDFs coloured by group
p3 = ggplot(df, aes("x", color="g")) + stat_ecdf()
print(p3)

# Weighted vs unweighted ECDF
weighted = pd.DataFrame({
    "x": np.arange(1, 11),
    "weights": [1, 2, 3, 4, 5, 5, 4, 3, 2, 1],
})
plain = pd.DataFrame({"x": np.repeat(weighted["x"].values, weighted["weights"].values)})

p4 = (
    ggplot(plain, aes("x"))
    + stat_ecdf(size=1)
    + stat_ecdf(aes(weight="weights"), data=weighted, color="green")
)
print(p4)
