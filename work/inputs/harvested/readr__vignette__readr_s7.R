# r2py crawler metadata
# package: readr
# source_type: vignette
# topic: readr_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\doc\readr.R
# lines: 5

suppressPackageStartupMessages(library(readr))
guess_parser(c("a", "b", "c"))
guess_parser(c("1", "2", "3"))
guess_parser(c("1,000", "2,000", "3,000"))
guess_parser(c("2001/10/10"))