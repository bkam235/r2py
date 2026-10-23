# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_spoke.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
df <- expand.grid(x = 1:10, y=1:10)

set.seed(1)
df$angle <- runif(100, 0, 2*pi)
df$speed <- runif(100, 0, sqrt(0.1 * df$x))

ggplot(df, aes(x, y)) +
  geom_point() +
  geom_spoke(aes(angle = angle), radius = 0.5)

ggplot(df, aes(x, y)) +
  geom_point() +
  geom_spoke(aes(angle = angle, radius = speed))