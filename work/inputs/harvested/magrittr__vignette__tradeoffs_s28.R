# r2py crawler metadata
# package: magrittr
# source_type: vignette
# topic: tradeoffs_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\magrittr\doc\tradeoffs.R
# lines: 5

suppressPackageStartupMessages(library(magrittr))
foo <- FALSE
NA %!>% { foo <- TRUE; . }

foo