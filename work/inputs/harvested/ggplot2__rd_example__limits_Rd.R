# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: limits.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 6

suppressPackageStartupMessages(library(ggplot2))
ggplot2:::limits(c(1, 5), "x")
ggplot2:::limits(c(5, 1), "x")
ggplot2:::limits(c("A", "b", "c"), "x")
ggplot2:::limits(c("A", "b", "c"), "fill")
ggplot2:::limits(as.Date(c("2008-01-01", "2009-01-01")), "x")