# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: cut_interval.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 12

suppressPackageStartupMessages(library(ggplot2))
table(cut_interval(1:100, 10))
table(cut_interval(1:100, 11))

set.seed(1)

table(cut_number(runif(1000), 10))

table(cut_width(runif(1000), 0.1))
table(cut_width(runif(1000), 0.1, boundary = 0))
table(cut_width(runif(1000), 0.1, center = 0))
table(cut_width(runif(1000), 0.1, labels = FALSE))