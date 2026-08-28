# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ggplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 57

import numpy as np
import pandas as pd
from plotnine import ggplot, aes, geom_point

# Create a data frame with some sample data, then create a data frame
# containing the mean value for each group in the sample data.
np.random.seed(1)

sample_df = pd.DataFrame({
    "group": pd.Categorical(np.repeat(["a", "b", "c"], 10)),
    "value": np.random.randn(30),
})

group_means_df = (
    sample_df
    .groupby("group", observed=True)["value"]
    .mean()
    .reset_index()
    .rename(columns={"value": "group_mean"})
)

# The following three code blocks create the same graphic, each using one
# of the three patterns specified above. In each graphic, the sample data
# are plotted in the first layer and the group means data frame is used to
# plot larger red points on top of the sample data in the second layer.

# Pattern 1
# Both the `data` and `mapping` arguments are passed into the `ggplot()`
# call. Those arguments are omitted in the first `geom_point()` layer
# because they get passed along from the `ggplot()` call. Note that the
# second `geom_point()` layer re-uses the `x = group` aesthetic through
# that mechanism but overrides the y-position aesthetic.
(
    ggplot(sample_df, aes(x="group", y="value"))
    + geom_point()
    + geom_point(aes(y="group_mean"), data=group_means_df, color="red", size=3)
)

# Pattern 2
# Same plot as above, passing only the `data` argument into the `ggplot()`
# call. The `mapping` arguments are now required in each `geom_point()`
# layer because there is no `mapping` argument passed along from the
# `ggplot()` call.
(
    ggplot(sample_df)
    + geom_point(aes(x="group", y="value"))
    + geom_point(
        aes(x="group", y="group_mean"),
        data=group_means_df,
        color="red",
        size=3,
    )
)

# Pattern 3
# Same plot as above, passing neither the `data` or `mapping` arguments
# into the `ggplot()` call. Both those arguments are now required in
# each `geom_point()` layer. This pattern can be particularly useful when
# creating more complex graphics with many layers using data from multiple
# data frames.
(
    ggplot()
    + geom_point(aes(x="group", y="value"), data=sample_df)
    + geom_point(
        aes(x="group", y="group_mean"),
        data=group_means_df,
        color="red",
        size=3,
    )
)
