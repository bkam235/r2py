# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: tradeoffs_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\tradeoffs.R
# lines: 4

suppressPackageStartupMessages(library(magrittr))
factory <- function(x) function() x
fn <- factory(TRUE)
fn()