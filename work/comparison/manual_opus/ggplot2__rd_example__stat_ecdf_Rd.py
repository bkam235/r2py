# r2py crawler metadata
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
    "g": pd.Categorical(np.repeat(["1", "2"], 100)),
})

(
    ggplot(df, aes(x="x"))
    + stat_ecdf(geom="step")
)

# Don't go to positive/negative infinity
(
    ggplot(df, aes(x="x"))
    + stat_ecdf(geom="step", pad=False)
)

# Multiple ECDFs
(
    ggplot(df, aes(x="x", colour="g"))
    + stat_ecdf()
)

# Using weighted eCDF
weighted = pd.DataFrame({"x": range(1, 11), "weights": list(range(1, 6)) + list(range(5, 0, -1))})
plain = pd.DataFrame({"x": np.repeat(weighted["x"].values, weighted["weights"].values)})

(
    ggplot(plain, aes(x="x"))
    + stat_ecdf(size=1)
    + stat_ecdf(aes(weight="weights"), data=weighted, colour="green")
)
