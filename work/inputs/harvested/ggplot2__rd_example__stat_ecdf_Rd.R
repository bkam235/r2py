# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_ecdf.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 27

suppressPackageStartupMessages(library(ggplot2))
set.seed(1)
df <- data.frame(
  x = c(rnorm(100, 0, 3), rnorm(100, 0, 10)),
  g = gl(2, 100)
)
ggplot(df, aes(x)) +
  stat_ecdf(geom = "step")

# Don't go to positive/negative infinity
ggplot(df, aes(x)) +
  stat_ecdf(geom = "step", pad = FALSE)

# Multiple ECDFs
ggplot(df, aes(x, colour = g)) +
  stat_ecdf()

# Using weighted eCDF
weighted <- data.frame(x = 1:10, weights = c(1:5, 5:1))
plain <- data.frame(x = rep(weighted$x, weighted$weights))

ggplot(plain, aes(x)) +
  stat_ecdf(linewidth = 1) +
  stat_ecdf(
    aes(weight = weights),
    data = weighted, colour = "green"
  )