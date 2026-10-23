# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_custom.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 23

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(mpg, aes(displ, hwy)) +
  geom_point()

# Define a graphical object
circle <- grid::circleGrob()

# Rendering a grob as a guide
p + guides(custom = guide_custom(circle, title = "My circle"))

# Controlling the size of the grob defined in relative units
p + guides(custom = guide_custom(
  circle, title = "My circle",
  width = unit(2, "cm"), height = unit(2, "cm"))
)

# Size of grobs in absolute units is taken directly without the need to
# set these manually
p + guides(custom = guide_custom(
  title = "My circle",
  grob = grid::circleGrob(r = unit(1, "cm"))
))