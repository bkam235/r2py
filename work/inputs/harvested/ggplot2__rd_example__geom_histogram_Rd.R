# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_histogram.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 93

suppressPackageStartupMessages(library(ggplot2))
ggplot(diamonds, aes(carat)) +
  geom_histogram()
ggplot(diamonds, aes(carat)) +
  geom_histogram(binwidth = 0.01)
ggplot(diamonds, aes(carat)) +
  geom_histogram(bins = 200)
# Map values to y to flip the orientation
ggplot(diamonds, aes(y = carat)) +
  geom_histogram()

# For histograms with tick marks between each bin, use `geom_bar()` with
# `scale_x_binned()`.
ggplot(diamonds, aes(carat)) +
  geom_bar() +
  scale_x_binned()

# Rather than stacking histograms, it's easier to compare frequency
# polygons
ggplot(diamonds, aes(price, fill = cut)) +
  geom_histogram(binwidth = 500)
ggplot(diamonds, aes(price, colour = cut)) +
  geom_freqpoly(binwidth = 500)

# To make it easier to compare distributions with very different counts,
# put density on the y axis instead of the default count
ggplot(diamonds, aes(price, after_stat(density), colour = cut)) +
  geom_freqpoly(binwidth = 500)


# When using the non-equal-width bins, we should set the area of the bars to
# represent the counts (not the height).
# Here we're using 10 equi-probable bins:
price_bins <- quantile(diamonds$price, probs = seq(0, 1, length = 11))

ggplot(diamonds, aes(price)) +
  geom_histogram(breaks = price_bins, color = "black") # misleading (height = count)

ggplot(diamonds, aes(price, after_stat(count / width))) +
  geom_histogram(breaks = price_bins, color = "black") # area = count

if (require("ggplot2movies")) {
# Often we don't want the height of the bar to represent the
# count of observations, but the sum of some other variable.
# For example, the following plot shows the number of movies
# in each rating.
m <- ggplot(movies, aes(rating))
m + geom_histogram(binwidth = 0.1)

# If, however, we want to see the number of votes cast in each
# category, we need to weight by the votes variable
m +
  geom_histogram(aes(weight = votes), binwidth = 0.1) +
  ylab("votes")

# For transformed scales, binwidth applies to the transformed data.
# The bins have constant width on the transformed scale.
m +
 geom_histogram() +
 scale_x_log10()
m +
  geom_histogram(binwidth = 0.05) +
  scale_x_log10()

# For transformed coordinate systems, the binwidth applies to the
# raw data. The bins have constant width on the original scale.

# Using log scales does not work here, because the first
# bar is anchored at zero, and so when transformed becomes negative
# infinity. This is not a problem when transforming the scales, because
# no observations have 0 ratings.
m +
  geom_histogram(boundary = 0) +
  coord_transform(x = "log10")
# Use boundary = 0, to make sure we don't take sqrt of negative values
m +
  geom_histogram(boundary = 0) +
  coord_transform(x = "sqrt")

# You can also transform the y axis.  Remember that the base of the bars
# has value 0, so log transformations are not appropriate
m <- ggplot(movies, aes(x = rating))
m +
  geom_histogram(binwidth = 0.5) +
  scale_y_sqrt()
}

# You can specify a function for calculating binwidth, which is
# particularly useful when faceting along variables with
# different ranges because the function will be called once per facet
ggplot(economics_long, aes(value)) +
  facet_wrap(~variable, scales = 'free_x') +
  geom_histogram(binwidth = \(x) 2 * IQR(x) / (length(x)^(1/3)))