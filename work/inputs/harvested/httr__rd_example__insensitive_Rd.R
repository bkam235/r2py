# r2py crawler metadata
# package: httr
# source_type: rd_example
# topic: insensitive.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\httr\help
# lines: 6

suppressPackageStartupMessages(library(httr))
x <- c("abc" = 1, "def" = 2)
x["ABC"]
y <- insensitive(x)
y["ABC"]
y[["ABC"]]