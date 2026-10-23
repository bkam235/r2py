# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: guide_bins.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 25

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mtcars) +
  geom_point(aes(disp, mpg, size = hp)) +
  scale_size_binned()

# Standard look
p

# Remove the axis or style it
p + guides(size = guide_bins(
  theme = theme(legend.axis.line = element_blank())
))

p + guides(size = guide_bins(show.limits = TRUE))

my_arrow <- arrow(length = unit(1.5, "mm"), ends = "both")
p + guides(size = guide_bins(
  theme = theme(legend.axis.line = element_line(arrow = my_arrow))
))

# Guides are merged together if possible
ggplot(mtcars) +
  geom_point(aes(disp, mpg, size = hp, colour = hp)) +
  scale_size_binned() +
  scale_colour_binned(guide = "bins")