# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: summarise_plot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 10

suppressPackageStartupMessages(library(ggplot2))
p <-
  ggplot(mpg, aes(displ, hwy)) +
  geom_point() +
  facet_wrap(~class)
b <- ggplot_build(p)

summarise_layout(b)
summarise_coord(b)
summarise_layers(b)