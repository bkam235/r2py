# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: lims.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 52

suppressPackageStartupMessages(library(ggplot2))
# Zoom into a specified area
ggplot(mtcars, aes(mpg, wt)) +
  geom_point() +
  xlim(15, 20)

# reverse scale
ggplot(mtcars, aes(mpg, wt)) +
  geom_point() +
  xlim(20, 15)

# with automatic lower limit
ggplot(mtcars, aes(mpg, wt)) +
  geom_point() +
  xlim(NA, 20)

# You can also supply limits that are larger than the data.
# This is useful if you want to match scales across different plots
small <- subset(mtcars, cyl == 4)
big <- subset(mtcars, cyl > 4)

ggplot(small, aes(mpg, wt, colour = factor(cyl))) +
  geom_point() +
  lims(colour = c("4", "6", "8"))

ggplot(big, aes(mpg, wt, colour = factor(cyl))) +
  geom_point() +
  lims(colour = c("4", "6", "8"))

# There are two ways of setting the axis limits: with limits or
# with coordinate systems. They work in two rather different ways.

set.seed(1)
last_month <- Sys.Date() - 0:59
df <- data.frame(
  date = last_month,
  price = c(rnorm(30, mean = 15), runif(30) + 0.2 * (1:30))
)

p <- ggplot(df, aes(date, price)) +
  geom_line() +
  stat_smooth()

p

# Setting the limits with the scale discards all data outside the range.
p + lims(x= c(Sys.Date() - 30, NA), y = c(10, 20))

# For changing x or y axis limits **without** dropping data
# observations use [coord_cartesian()]. Setting the limits on the
# coordinate system performs a visual zoom.
p + coord_cartesian(xlim =c(Sys.Date() - 30, NA), ylim = c(10, 20))