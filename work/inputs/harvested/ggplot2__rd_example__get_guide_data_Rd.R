# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: get_guide_data.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 20

suppressPackageStartupMessages(library(ggplot2))
# A standard plot
p <- ggplot(mtcars) +
  aes(mpg, disp, colour = drat, size = drat) +
  geom_point() +
  facet_wrap(vars(cyl), scales = "free_x")

# Guide information for legends
get_guide_data(p, "size")

# Note that legend guides can be merged
merged <- p + guides(colour = "legend")
get_guide_data(merged, "size")

# Guide information for positions
get_guide_data(p, "x", panel = 2)

# Coord polar doesn't support proper guides, so we get a list
polar <- p + coord_polar()
get_guide_data(polar, "theta", panel = 2)