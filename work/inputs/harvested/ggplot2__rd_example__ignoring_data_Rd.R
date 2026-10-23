# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: ignoring_data.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 10

suppressPackageStartupMessages(library(ggplot2))
data <- list(
  data.frame(x = 1:3, y = I(1:3)),
  data.frame(w = I(1:3), z = 1:3)
)

ignored <- .ignore_data(data)
str(ignored)

.expose_data(ignored)