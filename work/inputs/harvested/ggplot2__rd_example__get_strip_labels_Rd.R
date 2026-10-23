# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: get_strip_labels.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
# Basic plot
p <- ggplot(mpg, aes(displ, hwy)) +
  geom_point()

get_strip_labels(p) # empty facets
get_strip_labels(p + facet_wrap(year ~ cyl))
get_strip_labels(p + facet_grid(year ~ cyl))