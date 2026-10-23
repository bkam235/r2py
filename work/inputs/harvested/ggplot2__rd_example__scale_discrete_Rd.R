# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: scale_discrete.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 43

suppressPackageStartupMessages(library(ggplot2))
ggplot(diamonds, aes(cut)) + geom_bar()


# The discrete position scale is added automatically whenever you
# have a discrete position.

(d <- ggplot(subset(diamonds, carat > 1), aes(cut, clarity)) +
      geom_jitter())

d + scale_x_discrete("Cut")
d +
  scale_x_discrete(
    "Cut",
    labels = c(
      "Fair" = "F",
      "Good" = "G",
      "Very Good" = "VG",
      "Perfect" = "P",
      "Ideal" = "I"
    )
  )

# Use limits to adjust the which levels (and in what order)
# are displayed
d + scale_x_discrete(limits = c("Fair","Ideal"))

# you can also use the short hand functions xlim and ylim
d + xlim("Fair","Ideal", "Good")
d + ylim("I1", "IF")

# See ?reorder to reorder based on the values of another variable
ggplot(mpg, aes(manufacturer, cty)) +
  geom_point()
ggplot(mpg, aes(reorder(manufacturer, cty), cty)) +
  geom_point()
ggplot(mpg, aes(reorder(manufacturer, displ), cty)) +
  geom_point()

# Use abbreviate as a formatter to reduce long names
ggplot(mpg, aes(reorder(manufacturer, displ), cty)) +
  geom_point() +
  scale_x_discrete(labels = abbreviate)