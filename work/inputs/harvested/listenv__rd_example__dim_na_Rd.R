# r2py crawler metadata
# package: listenv
# source_type: rd_example
# topic: dim_na.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\listenv\help
# lines: 4

suppressPackageStartupMessages(library(listenv))
x <- 1:6
dim_na(x) <- c(2, NA)
print(dim(x))  ## [1] 2 3