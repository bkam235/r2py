# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_axis_stack.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(mpg, aes(displ, hwy)) +
  geom_point() +
  theme(axis.line = element_line())

# A normal axis first, then a capped axis
p + guides(x = guide_axis_stack("axis", guide_axis(cap = "both")))