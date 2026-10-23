# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: labs.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 30

suppressPackageStartupMessages(library(ggplot2))
p <- ggplot(mtcars, aes(mpg, wt, colour = cyl)) + geom_point()
p + labs(colour = "Cylinders")
p + labs(x = "New x label")

# Set labels by variable name instead of aesthetic
p + labs(dictionary = c(
  disp = "Displacment", # Not in use
  cyl  = "Number of cylinders",
  mpg  = "Miles per gallon",
  wt   = "Weight (1000 lbs)"
))

# The plot title appears at the top-left, with the subtitle
# display in smaller text underneath it
p + labs(title = "New plot title")
p + labs(title = "New plot title", subtitle = "A subtitle")

# The caption appears in the bottom-right, and is often used for
# sources, notes or copyright
p + labs(caption = "(based on data from ...)")

# The plot tag appears at the top-left, and is typically used
# for labelling a subplot with a letter.
p + labs(title = "title", tag = "A")

# If you want to remove a label, set it to NULL.
p +
 labs(title = "title") +
 labs(title = NULL)