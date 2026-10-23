# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: window-functions_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\window-functions.R
# lines: 4

suppressPackageStartupMessages(library(dplyr))
x <- 1:10
y <- 10:1
order_by(y, cumsum(x))