# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: geom_contour.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 27

suppressPackageStartupMessages(library(ggplot2))
# Basic plot
v <- ggplot(faithfuld, aes(waiting, eruptions, z = density))
v + geom_contour()

# Or compute from raw data
ggplot(faithful, aes(waiting, eruptions)) +
  geom_density_2d()


# use geom_contour_filled() for filled contours
v + geom_contour_filled()

# Setting bins creates evenly spaced contours in the range of the data
v + geom_contour(bins = 3)
v + geom_contour(bins = 5)

# Setting binwidth does the same thing, parameterised by the distance
# between contours
v + geom_contour(binwidth = 0.01)
v + geom_contour(binwidth = 0.001)

# Other parameters
v + geom_contour(aes(colour = after_stat(level)))
v + geom_contour(colour = "red")
v + geom_raster(aes(fill = density)) +
  geom_contour(colour = "white")