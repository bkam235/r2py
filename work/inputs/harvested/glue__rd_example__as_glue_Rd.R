# r2py crawler metadata
# package: glue
# source_type: rd_example
# topic: as_glue.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\glue\help
# lines: 7

suppressPackageStartupMessages(library(glue))
x <- as_glue(c("abc", "\"\\\\", "\n"))
x

x <- 1
y <- 3
glue("x + y") + " = {x + y}"