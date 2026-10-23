# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: rename.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 7

suppressPackageStartupMessages(library(plyr))
x <- c("a" = 1, "b" = 2, d = 3, 4)
# Rename column d to "c", updating the variable "x" with the result
x <- rename(x, replace = c("d" = "c"))
x
# Rename column "disp" to "displacement"
rename(mtcars, c("disp" = "displacement"))