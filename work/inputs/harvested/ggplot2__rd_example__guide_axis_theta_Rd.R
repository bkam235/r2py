# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_axis_theta.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
# A plot using coord_radial
p <- ggplot(mtcars, aes(disp, mpg)) +
  geom_point() +
  coord_radial()

# The `angle` argument can be used to set relative angles
p + guides(theta = guide_axis_theta(angle = 0))