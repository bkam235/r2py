# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: gg-add.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 12

suppressPackageStartupMessages(library(ggplot2))
base <-
 ggplot(mpg, aes(displ, hwy)) +
 geom_point()
base + geom_smooth()

# To override the data, you must use %+%
base %+% subset(mpg, fl == "p")

# Alternatively, you can add multiple components with a list.
# This can be useful to return from a function.
base + list(subset(mpg, fl == "p"), geom_smooth())