# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: translate_shape_string.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 5

suppressPackageStartupMessages(library(ggplot2))
translate_shape_string(c("circle", "square", "triangle"))

# Strings with 1 or less characters are interpreted as symbols
translate_shape_string(c("a", "b", "?"))