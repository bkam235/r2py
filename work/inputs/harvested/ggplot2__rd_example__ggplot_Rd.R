# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ggplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 57

suppressPackageStartupMessages(library(ggplot2))
# Create a data frame with some sample data, then create a data frame
# containing the mean value for each group in the sample data.
set.seed(1)

sample_df <- data.frame(
  group = factor(rep(letters[1:3], each = 10)),
  value = rnorm(30)
)

group_means_df <- setNames(
  aggregate(value ~ group, sample_df, mean),
  c("group", "group_mean")
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
ggplot(data = sample_df, mapping = aes(x = group, y = value)) +
  geom_point() +
  geom_point(
    mapping = aes(y = group_mean), data = group_means_df,
    colour = 'red', size = 3
  )

# Pattern 2
# Same plot as above, passing only the `data` argument into the `ggplot()`
# call. The `mapping` arguments are now required in each `geom_point()`
# layer because there is no `mapping` argument passed along from the
# `ggplot()` call.
ggplot(data = sample_df) +
  geom_point(mapping = aes(x = group, y = value)) +
  geom_point(
    mapping = aes(x = group, y = group_mean), data = group_means_df,
    colour = 'red', size = 3
  )

# Pattern 3
# Same plot as above, passing neither the `data` or `mapping` arguments
# into the `ggplot()` call. Both those arguments are now required in
# each `geom_point()` layer. This pattern can be particularly useful when
# creating more complex graphics with many layers using data from multiple
# data frames.
ggplot() +
  geom_point(mapping = aes(x = group, y = value), data = sample_df) +
  geom_point(
    mapping = aes(x = group, y = group_mean), data = group_means_df,
    colour = 'red', size = 3
  )