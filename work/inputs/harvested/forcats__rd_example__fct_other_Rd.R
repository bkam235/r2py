# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_other.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 5

suppressPackageStartupMessages(library(forcats))
x <- factor(rep(LETTERS[1:9], times = c(40, 10, 5, 27, 1, 1, 1, 1, 1)))

fct_other(x, keep = c("A", "B"))
fct_other(x, drop = c("A", "B"))