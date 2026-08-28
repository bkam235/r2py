# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ggplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 57

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point

np.random.seed(1)

sample_df = pd.DataFrame({
    "group": pd.Categorical(["a"] * 10 + ["b"] * 10 + ["c"] * 10),
    "value": np.random.normal(size=30),
})

group_means_df = (
    sample_df.groupby("group", observed=True)["value"]
    .mean()
    .reset_index()
    .rename(columns={"value": "group_mean"})
)

# Pattern 1: data and mapping in ggplot(); layers inherit both
p1 = (
    ggplot(data=sample_df, mapping=aes(x="group", y="value"))
    + geom_point()
    + geom_point(mapping=aes(y="group_mean"), data=group_means_df, color="red", size=3)
)
print(p1)

# Pattern 2: only data in ggplot(); each layer supplies its own mapping
p2 = (
    ggplot(data=sample_df)
    + geom_point(mapping=aes(x="group", y="value"))
    + geom_point(mapping=aes(x="group", y="group_mean"), data=group_means_df, color="red", size=3)
)
print(p2)

# Pattern 3: nothing in ggplot(); each layer is fully self-contained
p3 = (
    ggplot()
    + geom_point(mapping=aes(x="group", y="value"), data=sample_df)
    + geom_point(mapping=aes(x="group", y="group_mean"), data=group_means_df, color="red", size=3)
)
print(p3)
