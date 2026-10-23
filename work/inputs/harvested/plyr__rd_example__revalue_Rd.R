# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: revalue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 7

suppressPackageStartupMessages(library(plyr))
x <- c("a", "b", "c")
revalue(x, c(a = "A", c = "C"))
revalue(x, c("a" = "A", "c" = "C"))

y <- factor(c("a", "b", "c", "a"))
revalue(y, c(a = "A", c = "C"))