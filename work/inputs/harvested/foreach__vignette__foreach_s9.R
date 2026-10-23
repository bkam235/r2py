# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 4

suppressPackageStartupMessages(library(foreach))
cfun <- function(a, b) NULL
x <- foreach(i=1:4, .combine='cfun') %do% rnorm(4)
x