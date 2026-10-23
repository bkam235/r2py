# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: layer.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 16

suppressPackageStartupMessages(library(ggplot2))
# geom calls are just a short cut for layer
ggplot(mpg, aes(displ, hwy)) + geom_point()
# shortcut for
ggplot(mpg, aes(displ, hwy)) +
  layer(
    geom = "point", stat = "identity", position = "identity",
    params = list(na.rm = FALSE)
  )

# use a function as data to plot a subset of global data
ggplot(mpg, aes(displ, hwy)) +
  layer(
    geom = "point", stat = "identity", position = "identity",
    data = head, params = list(na.rm = FALSE)
  )