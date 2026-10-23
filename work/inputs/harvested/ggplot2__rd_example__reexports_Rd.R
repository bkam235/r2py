# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: reexports.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 6

suppressPackageStartupMessages(library(ggplot2))
ggplot(mpg, aes(displ, hwy)) +
  geom_point(alpha = 0.5, colour = "blue")

ggplot(mpg, aes(displ, hwy)) +
  geom_point(colour = alpha("blue", 0.5))