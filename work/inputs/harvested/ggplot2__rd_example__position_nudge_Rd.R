# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: position_nudge.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 23

suppressPackageStartupMessages(library(ggplot2))
df <- data.frame(
  x = c(1,3,2,5),
  y = c("a","c","d","c")
)

ggplot(df, aes(x, y)) +
  geom_point() +
  geom_text(aes(label = y))

ggplot(df, aes(x, y)) +
  geom_point() +
  geom_text(aes(label = y), position = position_nudge(y = -0.1))

# Or, in brief
ggplot(df, aes(x, y)) +
  geom_point() +
  geom_text(aes(label = y), nudge_y = -0.1)

# For each text individually
ggplot(df, aes(x, y)) +
  geom_point() +
  geom_text(aes(label = y, nudge_y = c(-0.1, 0.1, -0.1, 0.1)))