# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: update_ggplot.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 14

suppressPackageStartupMessages(library(ggplot2))
# making a new method for the generic
# in this example, we enable adding text elements
S7::method(update_ggplot, list(element_text, class_ggplot)) <-
  function(object, plot, ...) {
    plot + theme(text = object)
  }

# we can now use `+` to add our object to a plot
ggplot(mpg, aes(displ, cty)) +
  geom_point() +
  element_text(colour = "red")

# clean-up