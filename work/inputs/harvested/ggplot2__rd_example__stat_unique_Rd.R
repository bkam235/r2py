# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: stat_unique.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 5

suppressPackageStartupMessages(library(ggplot2))
ggplot(mtcars, aes(vs, am)) +
  geom_point(alpha = 0.1)
ggplot(mtcars, aes(vs, am)) +
  geom_point(alpha = 0.1, stat = "unique")